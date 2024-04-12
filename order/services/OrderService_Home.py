from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from ..models import Order

def HomeOrder_Service(request):
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
        return render(request, 'order/order_table.html', {'page_obj': page_obj})