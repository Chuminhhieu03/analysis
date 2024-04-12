from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Q, Sum
from ..models import Customer
from order.models import Order
from django.core.paginator import Paginator

def HomeCustomer_Service(request):
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

        for customer in customers:
            customer.revenue = Order.objects.filter(
                customer=customer,
                status='2'
            ).aggregate(revenue=Sum('total'))['revenue'] or 0

        paginator = Paginator(customers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'customer/customer_table.htmL', {'page_obj': page_obj})