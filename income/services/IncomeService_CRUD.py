from django.shortcuts import render, redirect
from ..models import Income
from django.contrib import messages
from datetime import datetime


def IncomeAdd_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'income/add_income.html')
    if request.method == 'POST':
        user = request.user
        amount = request.POST['amount']
        date = request.POST['date']
        source = request.POST['source']
        description = request.POST['description']
        income = Income(user=user, amount=amount, date=datetime.strptime(
            date, '%d/%m/%Y'), source=source, description=description)
        income.save()
        messages.success(request, 'Thêm thu nhập thành công')
        return redirect('income')

def IncomeEdit_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        income = Income.objects.get(id=id)
        income.date = income.date.strftime('%d/%m/%Y')
        income.amount = int(income.amount)
        return render(request, 'income/edit_income.html', {'income': income})
    if request.method == 'POST':
        income = Income.objects.get(id=id)
        income.amount = request.POST['amount']
        date = request.POST['date']
        income.date = datetime.strptime(date, '%d/%m/%Y')
        income.source = request.POST['source']
        income.description = request.POST['description']
        income.save()
        messages.success(request, 'Chỉnh sửa thu nhập thành công')
        return redirect('income')


def IncomeDelete_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'POST':
        try:
            income = Income.objects.get(id=id)
            income.delete()
        except:
            messages.warning(request, 'Khoản thu nhập không tồn tại')
            return redirect('income')
        messages.success(request, 'Xóa thu nhập thành công')
        return redirect('income')