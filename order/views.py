from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Q
from .models import Order
from product.models import Product
from customer.models import Customer
from .models import Order, OrderDetail
from category.models import Category
from django.core.paginator import Paginator
from collections import defaultdict

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
        try :
            query_date = datetime.strptime(query, '%d/%m/%Y')
            orders = Order.objects.filter(
                Q(user=user) & 
                (
                    Q(create_date=query_date)
                )
            ).order_by('-date')
        except :
            orders = Order.objects.filter(
                Q(user=user) & 
                (
                    Q(customer_name__icontains=query) |
                    Q(total__icontains=query) | 
                    Q(discrption__icontains=query)
                )
            ).order_by('-updated_date')
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'order_table.htmL', {'page_obj': page_obj})
    
def add(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    if request.method == 'GET':
        products = Product.objects.filter(user=request.user)
        customers = Customer.objects.filter(user=request.user)
        return render(request, 'add_order.html', {'products': products, 'customers': customers})
    if request.method == 'POST':
        user = request.user
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(id=customer_id)
        discrption = request.POST.get('discrption')
        customer_name = customer.name
        total = 0
        products = request.POST.get('products')
        # convert json to dict
        products = eval(products)

        # Group products by id and sum quantities
        grouped_products = defaultdict(int)
        for item in products:
            grouped_products[item['id']] += int(item['quantity'])

        order = Order(user=user, customer=customer, discrption=discrption, customer_name=customer_name, total=total)
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

def detail(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userprofile.type == "0":
        messages.warning(request, "Bạn không phải tài khoản doanh nghiệp")
        return redirect('login')
    order = Order.objects.get(id=id)
    orderDetails = OrderDetail.objects.filter(order=order)
    return render(request, 'detail_order.html', {'order': order, 'orderDetails': orderDetails})