from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


def handleLoginServices(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "GET":
        return render(request, 'user/login.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            messages.warning(request, "Tài khoản không tồn tại")
            return render(request, 'user/login.html')
        if not user.is_active:
            messages.warning(request, "Tài khoản chưa được kích hoạt")
            return render(request, 'user/login.html')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.warning(request, "Mật khẩu không chính xác")
            return render(request, 'user/login.html')
        login(request, user)
        return redirect('/')
