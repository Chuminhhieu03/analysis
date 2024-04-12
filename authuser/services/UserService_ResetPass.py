from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib import messages
from ..utils import generate_token
from django.conf import settings
from django.contrib.auth.models import User


def ResetPass_Service(request):
    if request.method == "GET":
        return render(request, 'user/resetPassword.html')
    if request.method == "POST":
        email = request.POST['email']
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()  # Lấy người dùng đầu tiên trong danh sách
            email_subject = '[Lấy lại mật khẩu]'
            message = render_to_string('user/reset-user-password.html', {
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user)
            })
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, [email])
            email_message.send()
            messages.success(
                request, "Kiểm tra email của bạn để lấy lại mật khẩu")
            return render(request, 'user/login.html')
        else:
            messages.warning(request, "Email không tồn tại trong hệ thống")
            return render(request, 'user/login.html')


def ActivateAccount_Service(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Kích hoạt tài khoản thành công")
        return redirect('/user/login')
    messages.warning(request, "Bạn đã kích hoạt tài khoản rồi")
    return render(request, 'user/login.html')


def SetNewPassword_Service(request, uidb64, token):
    if request.method == "GET":
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(
                    request, "Link này không còn hiệu luực, vui lòng thử lại với link mới")
                return render(request, 'user/login.html')
        except DjangoUnicodeDecodeError as identifier:
            pass
        messages.success(request, "Vui lòng nhập mật khẩu mới")
        return render(request, 'user/set_new_password.html', context)
    if request.method == "POST":
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Mật khẩu không khớp")
            return render(request, 'user/set_new_password.html', context)
        # check valid password with condition that password must have at least 1 uppercase, 1 lowercase, 1 number and 1 special character
        if not any(char.isupper() for char in password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết hoa")
            return render(request, 'user/set_new_password.html', context)
        if not any(char.islower() for char in password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết thường")
            return render(request, 'user/set_new_password.html', context)
        if not any(char.isdigit() for char in password):
            messages.warning(request, "Mật khẩu phải có ít nhất 1 chữ số")
            return render(request, 'user/set_new_password.html', context)
        if not any(not char.isalnum() for char in password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự đặc biệt")
            return render(request, 'user/set_new_password.html', context)
        if len(password) < 8:
            messages.warning(
                request, "Mật khẩu phải có ít nhất 8 ký tự")
            return render(request, 'user/set_new_password.html', context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(
                request, "Mật khẩu của bạn đã được thay đổi thành công")
            return redirect('/user/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Một lỗi đã xảy ra, vui lòng thử lại")
            return render(request, 'user/set_new_password.html', context)
