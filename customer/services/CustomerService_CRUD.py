from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from ..models import Customer


def AddCustomer_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'customer/add_customer.html')
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

def EditCustomer_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    customer = Customer.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'customer/edit_customer.html', {'customer': customer})
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        image = request.FILES.get('image', '')
        if image != '':
            if image.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'gif'] :
                messages.warning(request, "Ảnh phải là file ảnh")
                return render(request, 'edit_custome')
        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.updated_at = datetime.now()
        if image != '':
            customer.image = image
        customer.save()
        messages.success(request, "Sửa khách hàng thành công")
        return redirect('customer')

def DeleteCustomer_Service(request, id):
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