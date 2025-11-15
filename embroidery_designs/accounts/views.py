# embroidery_designs/accounts/views.py
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def profile(request):
    return render(request, 'accounts/profile.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('design_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('design_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('design_list')
    return redirect('design_list')