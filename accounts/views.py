from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, PasswordChangeForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.full_name}! Your account has been created.')
            if user.is_seller:
                messages.info(request, 'Please complete your farm profile to start selling.')
                return redirect('farms:create_farm')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            if user.is_seller and not user.has_farm_profile:
                return redirect('farms:create_farm')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            if not user.check_password(form.cleaned_data['old_password']):
                messages.error(request, 'Current password is incorrect.')
            else:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('accounts:profile')
    else:
        form = PasswordChangeForm()
    return render(request, 'accounts/change_password.html', {'form': form})
