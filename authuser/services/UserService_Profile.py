
from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import datetime

def HomeProfile_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    return render(request, 'profile.html')

def EditProfile_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == "GET":
        return render(request, 'editprofile.html')
    if request.method == "POST":
        user = request.user
        avatar = request.FILES.get('avatar', "")
        fullname = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']
        dob = request.POST['birth']
        if avatar != "":
            if avatar.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'gif']:
                messages.warning(request, "Ảnh đại diện phải là file ảnh")
                return render(request, 'editprofile.html')
        if avatar:
            user.userprofile.avatar = avatar
        user.first_name = fullname
        user.userprofile.address = address
        user.userprofile.phone = phone
        user.date_joined = datetime.strptime(dob, '%d/%m/%Y')
        user.userprofile.save()
        user.save()
        messages.success(request, "Cập nhật thông tin thành công")
        return render(request, 'editprofile.html')