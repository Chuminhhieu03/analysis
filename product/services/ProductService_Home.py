from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from ..models import Product
from order.models import OrderDetail

def ProductHome_Service(request):
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

        for product in products:
            product.revenue = OrderDetail.objects.filter(
                product=product,
                order__status='2'
            ).aggregate(revenue=Sum('total'))['revenue'] or 0

        paginator = Paginator(products, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'product/product_table.html', {'page_obj': page_obj})