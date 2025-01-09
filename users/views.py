from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.models import User
from .models import Profile

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

    context = {
        'profile_user': profile_user,
        'is_owner': is_owner,
    }

    return render(request, 'users/profile.html', context)

# @login_required
# def edit_profile(request):
#     """View for editing the user's own profile."""
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile has been updated successfully!')
#             return redirect('profile', username=request.user.username)
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = ProfileForm(instance=request.user)

#     return render(request, 'users/edit_profile.html', {'form': form})

# @login_required
# def edit_profile(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile has been updated successfully!')
#             return redirect('profile', username=request.user.username)
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = ProfileForm(instance=profile)

#     return render(request, 'users/edit_profile.html', {'form': form})

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