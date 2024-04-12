from django.shortcuts import render, redirect
from ..models import Expenses
from django.contrib import messages
from datetime import datetime


def ExpenseAdd_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'expense/add_expenses.html')
    if request.method == 'POST':
        user = request.user
        amount = request.POST['amount']
        date = request.POST['date']
        source = request.POST['source']
        description = request.POST['description']
        expenses = Expenses(user=user, amount=amount, date=datetime.strptime(
            date, '%d/%m/%Y'), source=source, description=description)
        expenses.save()
        messages.success(request, 'Thêm chi tiêu thành công')
        return redirect('expenses')


def ExpenseEdit_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        expenses = Expenses.objects.get(id=id)
        expenses.date = expenses.date.strftime('%d/%m/%Y')
        expenses.amount = int(expenses.amount)
        return render(request, 'expense/edit_expenses.html', {'expenses': expenses})
    if request.method == 'POST':
        expenses = Expenses.objects.get(id=id)
        expenses.amount = request.POST['amount']
        date = request.POST['date']
        expenses.date = datetime.strptime(date, '%d/%m/%Y')
        expenses.source = request.POST['source']
        expenses.description = request.POST['description']
        expenses.save()
        messages.success(request, 'Chỉnh sửa chi tiêu thành công')
        return redirect('expenses')


def ExpenseDelete_Service(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'POST':
        try:
            expenses = Expenses.objects.get(id=id)
            expenses.delete()
        except:
            messages.warning(request, 'Khoản chi tiêu không tồn tại')
            return redirect('expenses')
        messages.success(request, 'Xóa chi tiêu thành công')
        return redirect('expenses')