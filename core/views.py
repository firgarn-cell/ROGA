from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ApplicationForm
from .models import Application

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def dashboard_view(request):
    applications = request.user.applications.all().order_by('-created_at')
    return render(request, 'core/dashboard.html', {'applications': applications})

@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'core/create_application.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')