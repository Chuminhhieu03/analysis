from django.contrib import messages
from django.shortcuts import redirect, render


def UpgradeHome_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.state == "2":
        messages.warning(
            request, "Yêu cầu nâng cấp tài khoản của bạn đang chờ duyệt")
        return redirect('upgrade_success')
    if request.user.userupgrade.state == "1":
        messages.warning(request, "Tài khoản của bạn đã được nâng cấp")
        return redirect('upgrade_success')
    if request.method == "GET":
        return render(request, 'upgrade/upgrade.html')
    if request.method == "POST":
        return render(request, 'upgrade/upgrade_checkout.html')


def UpgradeCheckOut_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.state == "2":
        messages.warning(
            request, "Yêu cầu nâng cấp tài khoản của bạn đang chờ duyệt")
        return redirect('upgrade_success')
    if request.user.userupgrade.state == "1":
        messages.warning(request, "Tài khoản của bạn đã được nâng cấp")
        return redirect('upgrade_success')
    if request.method == "GET":
        return render(request, 'upgrade/upgrade_checkout.html')
    if request.method == "POST":
        user = request.user
        if user is None:
            messages.warning(request, "Tài khoản không tồn tại")
            return redirect('upgrade')
        user.userupgrade.state = '2'
        user.userupgrade.save()
        messages.success(request, "Yêu cầu nâng cấp tài khoản đã được gửi")
        return redirect('upgrade_success')


def UpgradeSucces_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    return render(request, 'upgrade/upgrade_success.html')
