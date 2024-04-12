from django.contrib import messages
from django.shortcuts import redirect, render


def ChangePassword_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == "GET":
        return render(request, 'user/changepassword.html')
    if request.method == "POST":
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmNewPassword']
        user = request.user
        if not user.check_password(old_password):
            messages.warning(request, "Mật khẩu cũ không chính xác")
            return render(request, 'user/changepassword.html')
        if new_password != confirm_password:
            messages.warning(request, "Mật khẩu mới không khớp")
            return render(request, 'user/changepassword.html')
        # check valid password with condition that password must have at least 1 uppercase, 1 lowercase, 1 number and 1 special character
        if not any(char.isupper() for char in new_password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết hoa")
            return render(request, 'user/changepassword.html')
        if not any(char.islower() for char in new_password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết thường")
            return render(request, 'user/changepassword.html')
        if not any(char.isdigit() for char in new_password):
            messages.warning(request, "Mật khẩu phải có ít nhất 1 chữ số")
            return render(request, 'user/changepassword.html')
        if not any(not char.isalnum() for char in new_password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự đặc biệt")
            return render(request, 'user/changepassword.html')
        if len(new_password) < 8:
            messages.warning(
                request, "Mật khẩu phải có ít nhất 8 ký tự")
            return render(request, 'user/changepassword.html')
        user.set_password(new_password)
        user.save()
        messages.success(
            request, "Mật khẩu của bạn đã được thay đổi thành công")
        return redirect('/user/login')
