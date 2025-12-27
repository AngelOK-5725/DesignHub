# embroidery_designs/accounts/views.py

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from payments.models import Purchase
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)



def favorite_designs(requests):
    ...

@login_required
def profile(request):
    purchases = Purchase.objects.filter(
        user=request.user
    ).select_related('design').order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'purchases': purchases
    })



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
            messages.success(request, f'Вход выполнен успешно, {user.username}!')
            return redirect('design_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из аккаунта.')
    return redirect('design_list')

# --------------------------------------------

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Инструкции по сбросу пароля отправлены на ваш email')
        return super().get(request, *args, **kwargs)

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Ваш пароль был успешно сброшен')
        return super().get(request, *args, **kwargs)    

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль был успешно сброшен!')
        return super().form_valid(form)
    
class CustomPasswordResetView(auth_views.PasswordResetView):
    def form_valid(self, form):
        messages.success(self.request, 'Инструкции по сбросу пароля отправлены на ваш email!')
        return super().form_valid(form)