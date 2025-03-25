# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PhoneLoginForm
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from django.http import JsonResponse
import random

def index(request):
    return render(request, 'index.html')

def tmp(request):
    return render(request, 'tmp.html')

def yun(request):
    return render(request, 'yun.html')

def python_page(request):
    return render(request, 'python.html')

def send_sms_register_code(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        # 生成验证码
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # 使用会话存储验证码
        request.session['register_code'] = code
        request.session['register_phone'] = phone
        # 这里可以添加实际的短信发送逻辑，例如使用第三方短信服务
        # 示例：调用短信 API 发送验证码到 phone
        return JsonResponse({'success': True, 'message': '验证码已发送，请查收'})
    return JsonResponse({'success': False, 'message': '请求方法错误'})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        phone_number = request.POST.get('phone_number')
        code = request.POST.get('code')

        # 验证验证码
        stored_code = request.session.get('register_code')
        stored_phone = request.session.get('register_phone')
        if not stored_code or not stored_phone or stored_phone != phone_number or stored_code != code:
            messages.error(request, '验证码错误，请重新输入。')
            return render(request, 'index.html', {'register_form': form})

        # 完善注册逻辑，确保正确写入数据库
        if form.is_valid():
            user = form.save()
            # 可以在这里添加额外的用户信息处理，如发送欢迎邮件等
            messages.success(request, 'Registration successful. You can now log in.')
            # 清除会话中的验证码信息
            del request.session['register_code']
            del request.session['register_phone']
            return redirect('index')
        else:
            print(form.errors)
            messages.error(request, '表单验证失败，请检查输入信息。')
    else:
        form = RegistrationForm()
    return render(request, 'index.html', {'register_form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        # 完善登录逻辑，确保正确验证用户信息
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

from django.core.mail import send_mail
from django.conf import settings

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        # 完善找回密码逻辑，确保正确发送重置邮件
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                # 生成有效的重置密码链接，这里使用 Django 的内置方法
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f'{settings.BASE_URL}/reset_password/?uidb64={uid}&token={token}'
                send_mail(
                    'Password Reset',
                    f'Click the link to reset your password: {reset_link}',
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

# 模拟发送短信验证码的函数
def send_sms_login_code(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        # 生成验证码
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # 存储验证码
        VERIFICATION_CODES[phone] = code
        # 这里可以添加实际的短信发送逻辑，例如使用第三方短信服务
        # 示例：调用短信 API 发送验证码到 phone
        return JsonResponse({'success': True, 'message': '验证码已发送，请查收'})
    return JsonResponse({'success': False, 'message': '请求方法错误'})

def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                # 生成验证码
                code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                if send_sms(phone_number, code):
                    # 这里可以将验证码保存到 session 中，用于后续验证
                    request.session['phone_verification_code'] = code
                    request.session['phone_number'] = phone_number
                    messages.success(request, 'Verification code sent to your phone.')
                else:
                    messages.error(request, 'Failed to send verification code.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Phone number not found.')
    else:
        form = PhoneLoginForm()
    return render(request, 'index.html', {'phone_login_form': form})
