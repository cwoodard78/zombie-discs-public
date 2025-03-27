import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.db import models
from django.contrib.auth.models import User
from .models import Profile
from disc.models import Disc

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

def home(request):
    if request.user.is_authenticated:
        # Fetch lost and found discs for the logged-in user
        lost_discs = Disc.objects.filter(status="lost")
        found_discs = Disc.objects.filter(status="found")

        context = {
            "lost_discs": lost_discs,
            "found_discs": found_discs,
        }
        return render(request, "user_home.html", context)
    else:
        # Fetch stats for the guest view
        stats_api_url = f"{request.build_absolute_uri('/discs/api/stats/')}"
        try:
            response = requests.get(stats_api_url)
            response.raise_for_status()
            stats = response.json()
        except requests.exceptions.RequestException as e:
            stats = {"total_lost": 0, "total_found": 0, "total_users": 0}
            print(f"Error fetching stats: {e}")

        context = {
            "total_lost": stats.get("total_lost", 0),
            "total_found": stats.get("total_found", 0),
            "total_users": stats.get("total_users", 0),
        }
        return render(request, "guest_home.html", context)

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