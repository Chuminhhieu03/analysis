from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from ..models import Product
from category.models import Category

def AddProduct_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        multiCategories = Category.objects.filter(user=request.user)
        return render(request, 'product/add_product.html', {'multiCategories': multiCategories})
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

def EditProduct_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    product = Product.objects.get(id=id)
    if request.method == 'GET':
        multiCategories = Category.objects.filter(user=request.user)
        return render(request, 'product/edit_product.html', {'product': product, 'multiCategories': multiCategories})
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

def DeleteProduct_Service(request, id):
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