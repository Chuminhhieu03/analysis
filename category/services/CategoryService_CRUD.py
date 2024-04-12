from django.contrib import messages
from django.shortcuts import redirect, render
from ..models import Category
from datetime import datetime


def CategoryAdd_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'category/add_category.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        user = request.user
        Category.objects.create(
            name=name,
            description=description,
            user=user
        )
        messages.success(request, "Thêm loạt mặt hàng thành công")
        return redirect('category')


def EditCategory_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    category = Category.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'category/edit_category.html', {'category': category})
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category.name = name
        category.description = description
        category.updated_at = datetime.now()
        category.save()
        messages.success(request, "Sửa loại mặt hình thành công")
        return redirect('category')


def DeleteCategory_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, "Xóa loại mặt hàng thành công")
    return redirect('category')
