from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from .models import User
from profiles.models import StudentProfile, RecruiterProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_overview')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            uni_or_company = form.cleaned_data.get('university_or_company')
            headline = form.cleaned_data.get('headline_or_title')

            if role == User.Role.STUDENT:
                StudentProfile.objects.create(
                    user=user,
                    university=uni_or_company or "Global Tech University",
                    degree=headline or "B.Tech Computer Science",
                    passport_slug=user.username.lower()
                )
            elif role == User.Role.RECRUITER:
                RecruiterProfile.objects.create(
                    user=user,
                    company_name=uni_or_company or "Innovate AI Labs",
                    designation=headline or "Talent Acquisition Manager"
                )

            login(request, user)
            messages.success(request, f"Welcome to SkillPassport, {user.first_name}!")
            return redirect('dashboard_overview')
        else:
            messages.error(request, "Registration error. Please check form details.")
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_overview')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard_overview')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('home')

def demo_login_view(request, role):
    if role == 'student':
        user = User.objects.filter(username='alex_morgan').first()
    elif role == 'recruiter':
        user = User.objects.filter(username='recruiter_techcorp').first()
    else:
        user = User.objects.filter(is_superuser=True).first()

    if user:
        login(request, user)
        messages.success(request, f"Logged in as Demo {role.title()}: {user.get_full_name()}")
        if user.is_recruiter:
            return redirect('recruiter_dashboard')
        return redirect('dashboard_overview')
    else:
        messages.error(request, f"Demo account for {role} not found. Please run seed_data first.")
        return redirect('login')
