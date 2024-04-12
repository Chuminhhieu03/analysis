from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from ..models import Category

def HomeCategory_Service(request):
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