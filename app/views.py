from datetime import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views.generic import View
from income.models import Income
from expenses.models import Expenses
from django.db.models import Sum

# Create your views here.
def index(request):
    if request.method == 'GET':
        datenow = datetime.now()
        # get month of now 
        monthnow = datenow.month
        yearnow = datenow.year
        # create a sum of income, expense, profit of this month
        sum_income = Income.objects.filter(date__month=monthnow).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
       
        sum_expense = Expenses.objects.filter(date__month=monthnow).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        sum_profit = sum_income - sum_expense

        last_sum_income = Income.objects.filter(date__month=monthnow-1).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        last_sum_expense = Expenses.objects.filter(date__month=monthnow-1).filter(date__year=yearnow).aggregate(Sum('amount'))['amount__sum']
        last_sum_profit = last_sum_income - last_sum_expense

        percent_income = (sum_income-last_sum_income)/last_sum_income*100
        percent_expense = (sum_expense-last_sum_expense)/last_sum_expense*100
        percent_profit = (sum_profit-last_sum_profit)/last_sum_profit*100
        # create a format each 3 number have one ','   
        sum_income = "{:,}".format(sum_income)
        sum_expense = "{:,}".format(sum_expense)
        sum_profit = "{:,}".format(sum_profit)
        # format percent to 2 number after '.'
        percent_income = "{:.2f}".format(percent_income)
        percent_expense = "{:.2f}".format(percent_expense)
        percent_profit = "{:.2f}".format(percent_profit)
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
        

        data_this_month = [100, 200, 300]
        data_last_month = [150, 250, 350]
        data_this_year = [1000, 2000, 3000]
        data_last_year = [1500, 2500, 3500]

        return JsonResponse({
            'sumIncome': sum_income,
            'sumExpense': sum_expense,
            'sumProfit': sum_profit,
            'percentIncome': percent_income,
            'percentExpense': percent_expense,
            'percentProfit': percent_profit,
            'datathismonth': data_this_month,
            'datalastmonth': data_last_month,
            'datathisyear': data_this_year,
            'datalastyear': data_last_year,
        })
