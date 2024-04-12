from django.contrib import messages
from django.shortcuts import redirect, render
from ..models import FeedBack


def FeedBack_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == "GET":
        return render(request, 'feedback.html')
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        feedback = FeedBack(user=request.user, title=title, content=content,email=request.user.email,phone=request.user.userprofile.phone)
        feedback.save()
        messages.success(request, "Gửi phản hồi thành công, chúng tôi sẽ liên hệ với bạn sớm nhất")
        return render(request, 'feedback.html')