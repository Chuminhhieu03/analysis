from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import Order
from product.models import Product
from customer.models import Customer
from ..models import Order, OrderDetail
from collections import defaultdict

def AddOrder_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        products = Product.objects.filter(user=request.user)
        customers = Customer.objects.filter(user=request.user)
        return render(request, 'order/add_order.html', {'products': products, 'customers': customers})
    if request.method == 'POST':
        user = request.user
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(id=customer_id)
        discrption = request.POST.get('discrption')
        status = request.POST.get('status')
        customer_name = customer.name
        total = 0
        products = request.POST.get('products')
        # convert json to dict
        products = eval(products)

        # Group products by id and sum quantities
        grouped_products = defaultdict(int)
        for item in products:
            grouped_products[item['id']] += int(item['quantity'])

        order = Order(user=user, customer=customer, discrption=discrption, customer_name=customer_name, total=total, status=status)
        order.save()

        for product_id, quantity in grouped_products.items():
            product = Product.objects.get(id=product_id)
            total += product.price * quantity
            orderDetail = OrderDetail(order=order, product=product,product_name = product.name, product_price = product.price,  quantity=quantity, total=product.price * quantity)
            orderDetail.save()

        order.total = total
        order.save()
        messages.success(request, "Thêm đơn hàng thành công")
        return redirect('order')

def DetailOrder_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    order = Order.objects.get(id=id)
    orderDetails = OrderDetail.objects.filter(order=order)
    return render(request, 'order/detail_order.html', {'order': order, 'orderDetails': orderDetails})

def EditOrder_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        order = Order.objects.get(id=id)
        orderDetails = OrderDetail.objects.filter(order=order)
        products = Product.objects.filter(user=request.user)
        customers = Customer.objects.filter(user=request.user)
        return render(request, 'order/edit_order.html', {'order': order, 'orderDetails': orderDetails, 'products': products, 'customers': customers})
    if request.method == 'POST':
        #get id from url parameter
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(id=customer_id)
        discrption = request.POST.get('discrption')
        customer_name = customer.name
        status = request.POST.get('status')
        total = 0
        products = request.POST.get('products')
        # convert json to dict
        products = eval(products)

        # Group products by id and sum quantities
        grouped_products = defaultdict(int)
        for item in products:
            grouped_products[item['id']] += int(item['quantity'])

        order = Order.objects.get(id=id)
        order.customer = customer
        order.discrption = discrption
        order.customer_name = customer_name
        order.status = status
        order.total = total
        order.save()

        OrderDetail.objects.filter(order=order).delete()

        for product_id, quantity in grouped_products.items():
            product = Product.objects.get(id=product_id)
            total += product.price * quantity
            orderDetail = OrderDetail(order=order, product=product,product_name = product.name, product_price = product.price,  quantity=quantity, total=product.price * quantity)
            orderDetail.save()

        order.total = total
        order.save()
        messages.success(request, "Sửa đơn hàng thành công")
        return redirect('order')