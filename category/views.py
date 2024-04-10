from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Q
from .models import Category
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        query = request.GET.get('q', '')
        user = request.user
        categories = Category.objects.filter(
            Q(user=user) & 
            (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        ).order_by('-updated_at')
        paginator = Paginator(categories, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'category_table.htmL', {'page_obj': page_obj})

def add(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'add_category.html')
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

def edit(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    category = Category.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'edit_category.html', {'category': category})
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category.name = name
        category.description = description
        category.updated_at = datetime.now()
        category.save()
        messages.success(request, "Sửa loại mặt hình thành công")
        return redirect('category')

def delete(request, id):
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
