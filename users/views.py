import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q, F
from django.contrib.auth.models import User


from .forms import RegistrationForm, ProfileForm
from .models import Profile
from .serializers import UserSerializer
from .constants import FAQS
from disc.models import Disc, Reward, DiscMatch

from rest_framework.generics import ListAPIView

class UserListAPIView(ListAPIView):
    """
    API View to list all users and info
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

def get_paginated_discs(request, status, param_name):
    """
    Helper function to paginate discs based on their status.
    """
    queryset = Disc.objects.filter(status=status, state='active').order_by('-created_at')
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get(param_name, 1)
    return paginator.get_page(page_number)

def get_top_rewards(limit=5):
    """
    Return top rewards based on highest reward amounts.
    """
    return Reward.objects.filter(disc__state='active').order_by('-amount')[:limit]


def get_leaderboards(limit=5):
    """
    Return leaderboard data for lost, found, karma, rewards offered, and rewards earned.
    """
    # Lost discs in descending order up to limit
    lost = User.objects.annotate(
        lost_count=Count('disc', filter=Q(disc__status='lost'))
    ).filter(lost_count__gt=0).order_by('-lost_count')[:limit]

    # Found discs in descending order up to limit
    found = User.objects.annotate(
        found_count=Count('disc', filter=Q(disc__status='found'))
    ).filter(found_count__gt=0).order_by('-found_count')[:limit]

    # Most profile karma descending order up to limit
    karma = User.objects.select_related('profile').filter(
        profile__karma__gt=0
    ).order_by('-profile__karma')[:limit]

    # User who has offered the most rewards (descending)
    rewards_offered = (
        Reward.objects
        .select_related('disc__user')
        .values('disc__user__username')
        .annotate(
            username=F('disc__user__username'),
            total_rewards=Count('id'),
            total_amount=Sum('amount')
        )
        .order_by('-total_amount')[:limit]
    )

    # User who has collected the most rewards (descending)
    rewards_earned = (
        DiscMatch.objects
        .filter(
            lost_disc__reward__isnull=False,
            lost_disc__state='returned',
            found_disc__state='returned',
        )
        .values('found_disc__user__username')
        .annotate(
            username=F('found_disc__user__username'),
            total_earned=Sum('lost_disc__reward__amount'),
            found_count=Count('id')
        )
        .order_by('-total_earned')[:limit]
    )

    return lost, found, karma, rewards_offered, rewards_earned


def get_guest_stats(request):
    """
    Retrieve community stats via API for unauthenticated users.
    """
    stats_api_url = f"{request.build_absolute_uri('/discs/api/stats/')}"
    try:
        response = requests.get(stats_api_url)
        response.raise_for_status()
        stats = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stats: {e}")
        stats = {"total_lost": 0, "total_found": 0, "total_users": 0}
    return stats

def home(request):
    """
    Render user dashboard if authenticated, or guest home page with stats otherwise.
    """
    if request.user.is_authenticated:
        lost_discs = get_paginated_discs(request, 'lost', 'lost_page')
        found_discs = get_paginated_discs(request, 'found', 'found_page')
        active_tab = "found" if "found_page" in request.GET else "lost"
        top_rewards = get_top_rewards()
        lost_leaderboard, found_leaderboard, karma_leaderboard, rewards_offered, rewards_earned = get_leaderboards()

        context = {
            "lost_discs": lost_discs,
            "found_discs": found_discs,
            "top_rewards": top_rewards,
            "lost_leaderboard": lost_leaderboard,
            "found_leaderboard": found_leaderboard,
            "karma_leaderboard": karma_leaderboard,
            "rewards_offered": rewards_offered,
            "rewards_earned": rewards_earned,
            "active_tab": active_tab,
        }
        return render(request, "user_home.html", context)

    else:
        stats = get_guest_stats(request)
        return render(request, "guest_home.html", stats)

# ACCOUNT MANAGEMENT
def register(request):
    """
    Handle user registration with validation and success messaging
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Optional message
            # messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def profile(request, username):
    """
    View a public or private profile page
    """
    profile_user = get_object_or_404(User, username=username)
    # Check if the logged-in user is viewing their own profile
    is_owner = request.user == profile_user

    # Find disc stats
    lost_total = Disc.objects.filter(user=profile_user, status='lost').count()
    found_total = Disc.objects.filter(user=profile_user, status='found').count()
    karma = profile_user.profile.karma

    context = {
        'profile_user': profile_user,
        'is_owner': is_owner,
        'lost_total': lost_total,
        'found_total': found_total,
        'karma': karma,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    """
    Allow authenticated users to edit their profile   
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def delete_account(request):
    """
    Allow users to delete their account with confirmation
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')  # Redirect to guest home
    return render(request, 'users/delete_account.html')

@login_required
def award_karma(request, username):
    """
    Allow users to give karma to others
    """
    target_user = get_object_or_404(User, username=username)

    # Prevent self-award
    if request.user == target_user:
        messages.error(request, "You can't give yourself karma!")
        return redirect('profile', username=username)

    target_profile = target_user.profile
    target_profile.karma += 1
    target_profile.save()

    return redirect('profile', username=username)

def help_view(request):
    """
    Render the FAQ/help page
    """
    return render(request, "users/help.html", {"faqs": FAQS})