# embroidery_designs/accounts/views.py
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .forms import ProfileForm

# @login_required
# def edit_profile(request):
#     profile = request.user.profile
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # возвращаемся на страницу профиля
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, 'edit_profile.html', {'form': form})


def profile(request):
    return render(request, 'accounts/profile.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно. Вы вошли в систему.')
            login(request, user)
            return redirect('design_list')
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, исправьте ошибки ниже.')
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