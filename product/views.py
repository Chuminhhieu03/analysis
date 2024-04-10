from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Q
from .models import Product
from category.models import Category
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
        products = Product.objects.filter(
            Q(user=user) & 
            (
                Q(name__icontains=query) |
                Q(description__icontains=query) | 
                Q(price__icontains=query)
            )
        ).order_by('-updated_at')
        paginator = Paginator(products, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'product_table.htmL', {'page_obj': page_obj})

def add(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        multiCategories = Category.objects.filter(user=request.user)
        return render(request, 'add_product.html', {'multiCategories': multiCategories})
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        categoryId = request.POST.get('category')
        category = Category.objects.get(id=categoryId)
        try:
            image = request.FILES['image']
        except Exception as e:
            messages.warning(request, "Xảy ra lỗi chọn ảnh")
            return redirect('add_product')
        if image.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'gif']:
            messages.warning(request, "Ảnh phải là file ảnh")
            return render(request, 'add_product')
        user = request.user
        Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image,
            user=user
        )
        messages.success(request, "Thêm sản phẩm thành công")
        return redirect('product')

def edit(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    product = Product.objects.get(id=id)
    if request.method == 'GET':
        multiCategories = Category.objects.filter(user=request.user)
        return render(request, 'edit_product.html', {'product': product, 'multiCategories': multiCategories})
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image', '')
        if image != '':
            if image.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'gif'] :
                messages.warning(request, "Ảnh phải là file ảnh")
                return render(request, 'edit_product')
        product.name = name
        product.price = price
        product.description = description
        product.updated_at = datetime.now()
        if image != '':
            product.image = image
        product.save()
        messages.success(request, "Sửa sản phẩm thành công")
        return redirect('product')

def delete(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, "Xóa sản phẩm thành công")
    return redirect('product')