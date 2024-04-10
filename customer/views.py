from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Q
from .models import Customer
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
        customers = Customer.objects.filter(
            Q(user=user) & 
            (
                Q(name__icontains=query) |
                Q(phone__icontains=query) | 
                Q(address__icontains=query)
            )
        ).order_by('-updated_at')
        paginator = Paginator(customers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'customer_table.htmL', {'page_obj': page_obj})

def add(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'add_customer.html')
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        try:
            image = request.FILES['image']
        except Exception as e:
            messages.warning(request, "Xảy ra lỗi chọn ảnh")
            return redirect('add_customer')
        if image.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'gif']:
            messages.warning(request, "Ảnh phải là file ảnh")
            return render(request, 'add_customer')
        Customer.objects.create(
            name=name,
            phone=phone,
            address=address,
            image=image,
            user=user
        )
        messages.success(request, "Thêm khách hàng thành công")
        return redirect('customer')

def edit(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    customer = Customer.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'edit_customer.html', {'customer': customer})
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        try:
            image = request.FILES['image']
        except Exception as e:
            messages.warning(request, "Xảy ra lỗi chọn ảnh")
            return redirect('add_customer')
        if image.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'gif']:
            messages.warning(request, "Ảnh phải là file ảnh")
            return render(request, 'edit_customer')
        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.updated_at = datetime.now()
        if image:
            customer.image = image
        customer.save()
        messages.success(request, "Sửa khách hàng thành công")
        return redirect('customer')

def delete(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    customer = Customer.objects.get(id=id)
    customer.delete()
    messages.success(request, "Xóa khách hàng thành công")
    return redirect('customer')