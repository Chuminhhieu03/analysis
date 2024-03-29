from datetime import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views.generic import View
from income.models import Income
from expenses.models import Expenses
from django.db.models import Sum
from django.contrib import messages

# Create your views here.
def index(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        user = request.user
        datenow = datetime.now()
        # get month of now 
        monthnow = datenow.month
        yearnow = datenow.year
        # create a sum of income, expense, profit of this month
        sum_income = Income.objects.filter(user = user).filter(date__month=monthnow).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        sum_income = (sum_income or 0)
        sum_expense = Expenses.objects.filter(user = user).filter(date__month=monthnow).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        sum_expense = (sum_expense or 0)
        sum_profit = sum_income - sum_expense

        last_sum_income = Income.objects.filter(user = user).filter(date__month=monthnow-1).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        last_sum_income = (last_sum_income or 0)
        last_sum_expense = Expenses.objects.filter(user = user).filter(date__month=monthnow-1).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        last_sum_expense = (last_sum_expense or 0)
        last_sum_profit = last_sum_income - last_sum_expense

        if last_sum_income == 0:
            percent_income = (sum_income-last_sum_income)/1*100
        else:
            percent_income = (sum_income-last_sum_income)/last_sum_income*100
        if last_sum_expense == 0:
            percent_expense = (sum_expense-last_sum_expense)/1*100
        else:
            percent_expense = (sum_expense-last_sum_expense)/last_sum_expense*100
        if last_sum_profit == 0:
            percent_profit = (sum_profit-last_sum_profit)/1*100
        else:        
            percent_profit = (sum_profit-last_sum_profit)/last_sum_profit*100
        
        
        return render(request, 'index.html', {
            'sumIncome': sum_income,
            'sumExpense': sum_expense,
            'sumProfit': sum_profit,
            'percentIncome': percent_income,
            'percentExpense': percent_expense,
            'percentProfit': percent_profit,
        })
class GetData(View):
    def get(self, request, *args, **kwargs):
        # Get the username from the request parameters
        username = request.GET.get('p')
        user = request.user
        datenow = datetime.now()
        mothnow = datenow.month
        yearnow = datenow.year
        data_income_this_month = [0] * 31
        data_expense_this_month = [0] * 31
        data_income_this_year = [0] * 12
        data_expense_this_year = [0] * 12
        # get all data income for each month in a year
        for i in range(1,13):
            data_income_this_year[i-1] = Income.objects.filter(user = user).filter(date__month=i).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
            data_expense_this_year[i-1] = Expenses.objects.filter(user = user).filter(date__month=i).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        # get all data income for each day in a month
        for i in range(1,32):
            data_income_this_month[i-1] = Income.objects.filter(user = user).filter(date__day=i).filter(date__month=mothnow).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
            data_expense_this_month[i-1] = Expenses.objects.filter(user = user).filter(date__day=i).filter(date__month=mothnow).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        # Return the JSON response with the data
        return JsonResponse({
            'data_income_this_month': data_income_this_month,
            'data_expense_this_month': data_expense_this_month,
            'data_income_this_year': data_income_this_year,
            'data_expense_this_year': data_expense_this_year,
        })
