from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import Expenses
import json
from django.contrib import messages

def ExpenseChart_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    return render(request, 'expenses_chart.html')


def ExpenseDataChar_Service(request):
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
        expenses = Expenses.objects.filter(user=user, date__month=date.split(
            '/')[0], date__year=date.split('/')[1])
        # Create a dictionary to store the expenses data
        expenses_data = [0, 0, 0, 0]
        # Loop through the expenses data and add the amount to the corresponding source
        for i in expenses:
            if i.source == '0':
                expenses_data[0] += i.amount
            elif i.source == '1':
                expenses_data[1] += i.amount
            elif i.source == '2':
                expenses_data[2] += i.amount
            elif i.source == '3':
                expenses_data[3] += i.amount
        # Return the expenses data as a JSON response
        if sum(expenses_data) == 0 or len(expenses) == 0:
            messages.warning(request, "Chưa có dữ liệu chi tiêu cho tháng này")
            # return fail message
            return JsonResponse({'error': 'Chưa có dữ liệu chi tiêu cho tháng này'}, status=400)
        return JsonResponse(expenses_data, safe=False)