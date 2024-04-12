from django.shortcuts import render, redirect
from ..models import Income
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Q
from income.constVar import SOURCE_USER_ARR, SOURCE_BUSINESS_ARR

def IncomeHome_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        query = request.GET.get('q', '')
        user = request.user
        try:
            query_date = datetime.strptime(query, '%d/%m/%Y')
            incomes = Income.objects.filter(
                Q(user=user) &
                (
                    Q(date=query_date)
                )
            ).order_by('-date')
        except:
            if user.userprofile.type == "1":
                source_value = next((str(i) for i, item in enumerate(SOURCE_BUSINESS_ARR) if query.lower() in item.lower()), None)
            else:
                source_value = next((str(i) for i, item in enumerate(SOURCE_USER_ARR) if query.lower() in item.lower()), None)
            # return the source choices index if value contains query
            incomes = Income.objects.filter(
                Q(user=user) &
                (
                    Q(description__icontains=query) |
                    Q(amount__icontains=query) |
                    Q(source=source_value)
                )
            ).order_by('-date')
        paginator = Paginator(incomes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'income_table.html', {'page_obj': page_obj})