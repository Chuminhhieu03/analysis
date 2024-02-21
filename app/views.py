from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')
def income(request):
    return render(request, 'income_table.html')
def expense(request):
    return render(request, 'expense_table.html')
def add_info(request):
    return render(request, 'add_info.html')
