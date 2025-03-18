# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PhoneLoginForm # type: ignore
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

def index(request):
    return render(request, 'index.html')

def tmp(request):
    return render(request, 'tmp.html')

def yun(request):
    return render(request, 'yun.html')

def python_page(request):
    return render(request, 'python.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'index.html', {'register_form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('identifier')
            password = form.cleaned_data.get('password')
            try:
                if '@' in identifier:
                    user = CustomUser.objects.get(email=identifier)
                elif identifier.isdigit():
                    user = CustomUser.objects.get(phone_number=identifier)
                else:
                    user = CustomUser.objects.get(username=identifier)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
            except CustomUser.DoesNotExist:
                pass
            messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'index.html', {'login_form': form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                # 这里可以添加发送重置密码邮件的逻辑
                send_mail(
                    'Password Reset',
                    'Click the link to reset your password: [reset link]',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset email sent. Check your inbox.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Email not found.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'index.html', {'password_reset_form': form})

def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                # 这里可以添加发送验证码的逻辑
                messages.success(request, 'Verification code sent to your phone.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Phone number not found.')
    else:
        form = PhoneLoginForm()
    return render(request, 'index.html', {'phone_login_form': form})
