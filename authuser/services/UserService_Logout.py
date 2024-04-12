from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout

def LogOut_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    auth_logout(request)
    messages.info(request, "Đăng xuất thành công")
    return redirect('/user/login')