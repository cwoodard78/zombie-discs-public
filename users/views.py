import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.db import models
from django.contrib.auth.models import User
from .models import Profile
from disc.models import Disc, Reward
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q, F, Value, IntegerField

# For API
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserListAPIView(ListAPIView):
    """
    API View to list all users and email
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Count, Q
from disc.models import Disc, Reward, DiscMatch
import requests


def get_paginated_discs(request, status, param_name):
    queryset = Disc.objects.filter(status=status, state='active').order_by('-created_at')
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get(param_name, 1)
    return paginator.get_page(page_number)


def get_top_rewards(limit=5):
    return Reward.objects.filter(disc__state='active').order_by('-amount')[:limit]


def get_leaderboards(limit=5):
    lost = User.objects.annotate(
        lost_count=Count('disc', filter=Q(disc__status='lost'))
    ).order_by('-lost_count')[:limit]

    found = User.objects.annotate(
        found_count=Count('disc', filter=Q(disc__status='found'))
    ).order_by('-found_count')[:limit]

    karma = User.objects.select_related('profile').filter(
        profile__karma__gt=0
    ).order_by('-profile__karma')[:limit]

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

# def home(request):
#     if request.user.is_authenticated:
#         # Fetch lost and found discs sorted by most recent
#         lost_discs_qs = Disc.objects.filter(status="lost").order_by("-created_at")
#         found_discs_qs = Disc.objects.filter(status="found").order_by("-created_at")

#         lost_paginator = Paginator(lost_discs_qs, 5)
#         found_paginator = Paginator(found_discs_qs, 5)

#         lost_page_number = request.GET.get("lost_page", 1)
#         found_page_number = request.GET.get("found_page", 1)

#         lost_discs = lost_paginator.get_page(lost_page_number)
#         found_discs = found_paginator.get_page(found_page_number)

#         # Determine which tab to show based on which page param is set
#         active_tab = "found" if "found_page" in request.GET else "lost"

#         # Collect top rewards in decreasing order
#         top_rewards = Reward.objects.select_related('disc').order_by('-amount')[:5]

#         # Leaderboard: Users with most lost discs
#         lost_leaderboard = (
#             User.objects.annotate(lost_count=Count('disc', filter=Q(disc__status='lost')))
#             .order_by('-lost_count')[:5]
#         )

#         # Leaderboard: Users with most found discs
#         found_leaderboard = (
#             User.objects.annotate(found_count=Count('disc', filter=Q(disc__status='found')))
#             .order_by('-found_count')[:5]
#         )

#         karma_leaderboard = (
#             User.objects.select_related('profile')
#             .filter(profile__karma__gt=0)
#             .order_by('-profile__karma')[:5]
#         )

#         context = {
#             "lost_discs": lost_discs,
#             "found_discs": found_discs,
#             "top_rewards": top_rewards,
#             'lost_leaderboard': lost_leaderboard,
#             'found_leaderboard': found_leaderboard,
#             'karma_leaderboard': karma_leaderboard,
#             "active_tab": active_tab,
#         }
#         return render(request, "user_home.html", context)
    
#     else:
#         # Fetch stats for the guest view
#         stats_api_url = f"{request.build_absolute_uri('/discs/api/stats/')}"
#         try:
#             response = requests.get(stats_api_url)
#             response.raise_for_status()
#             stats = response.json()
#         except requests.exceptions.RequestException as e:
#             stats = {"total_lost": 0, "total_found": 0, "total_users": 0}
#             print(f"Error fetching stats: {e}")

#         context = {
#             "total_lost": stats.get("total_lost", 0),
#             "total_found": stats.get("total_found", 0),
#             "total_users": stats.get("total_users", 0),
#         }
#         return render(request, "guest_home.html", context)

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def profile(request, username):
    """View a public or private profile based on ownership."""
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
    profile, created = Profile.objects.get_or_create(user=request.user)

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
    """Allow users to delete their account with confirmation"""
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')  # Redirect to homepage or any other page after deletion
    return render(request, 'users/delete_account.html')

@login_required
def award_karma(request, username):
    target_user = get_object_or_404(User, username=username)

    # Prevent self-award
    if request.user == target_user:
        messages.error(request, "You can't give yourself karma!")
        return redirect('profile', username=username)

    target_profile = target_user.profile
    target_profile.karma += 1
    target_profile.save()

    messages.success(request, f"You gave karma to {target_user.username}! 🙌")
    return redirect('profile', username=username)

from django.shortcuts import render
from .constants import FAQS

def help_view(request):
    # faqs = [
    #     ("How do I submit a disc?",
    #      "Click 'Submit a Disc' from the top menu, fill out the form, and mark the disc's location on the map."),

    #     ("Can I edit or delete my disc listing?",
    #      "Yes, go to 'My Discs' and click on a disc to edit or archive it."),

    #     ("How do rewards work?",
    #      "You can offer an optional reward when submitting a lost disc. This is visible to anyone who finds it."),

    #     ("What do the status and state fields mean?",
    #      "<strong>Status:</strong> Lost or Found.<br><strong>State:</strong> Active (being tracked), Returned (matched), Archived (closed)."),

    #     ("Can I use my current location on the map?",
    #      "Yes! When submitting a disc, the map will try to center on your device's location."),
    # ]

    return render(request, "users/help.html", {"faqs": FAQS})