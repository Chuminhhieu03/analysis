from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from ..utils import generate_token
from django.conf import settings
from ..models import UserProfile, UserUpgrade


def SignUp_Service(request):
    if request.method == "GET":
        return render(request, 'user/signup.html')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        typeUser = request.POST['typeUser']
        # check username is already exist or not
        if User.objects.filter(username=username).exists():
            messages.warning(
                request, "Tài khoản này đã tồn tại trong hệ thống")
            return render(request, 'user/signup.html')
        # check email is already exist or not
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email này đã tồn tại")
            return render(request, 'user/signup.html')
        # check password is match or not
        if pass1 != pass2:
            messages.warning(request, "Mật khẩu không khớp")
            return render(request, 'user/signup.html')
        # create
        user = User.objects.create_user(
            username=username, email=email, password=pass1)
        user.first_name = f"Người dùng #{user.id}"
        user.is_active = False
        user.userprofile = UserProfile()
        user.userprofile.type = typeUser
        user.userprofile.save()
        user.userupgrade = UserUpgrade()
        user.userupgrade.save()
        user.save()
        email_subject = "Kích hoạt tài khoản"
        message = render_to_string('user/activate_account.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email_message = EmailMessage(
            email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()
        messages.success(
            request, "Tài khoản của bạn đã được tạo thành công, vui lòng kích hoạt")
        return render(request, 'user/login.html')
