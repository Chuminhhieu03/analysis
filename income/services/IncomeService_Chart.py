from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import Income
import json
from django.contrib import messages

def IncomeChart_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    return render(request, 'income/income_chart.html')

def IncomeDataChar_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        date = data.get('date')
        if date is None:
            return JsonResponse({'error': 'Missing date parameter'}, status=400)
        # Get the income data for the user and date provided by format mm/yyyy
        income = Income.objects.filter(user=user, date__month=date.split('/')[0], date__year=date.split('/')[1])
        # Create a dictionary to store the income data
        income_data = [0, 0, 0, 0]
        # Loop through the income data and add the amount to the corresponding source
        for i in income:
            if i.source == '0':
                income_data[0] += i.amount
            elif i.source == '1':
                income_data[1] += i.amount
            elif i.source == '2':
                income_data[2] += i.amount
            elif i.source == '3':
                income_data[3] += i.amount
        # Return the income data as a JSON response
        if sum(income_data) == 0 or len(income) == 0:
            messages.warning(request, "Chưa có dữ liệu thu nhập cho tháng này")
            # return fail message
            return JsonResponse({'error': 'Chưa có dữ liệu thu nhập cho tháng này'}, status=400)
        return JsonResponse(income_data, safe=False)