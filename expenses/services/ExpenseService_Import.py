from django.shortcuts import redirect
from ..models import Expenses
from django.contrib import messages
import pandas as pd
from decimal import Decimal

def ExpenseImport_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.upgrade == False:
        messages.warning(request, "Bạn chưa nâng cấp tài khoản")
        return redirect('upgrade')
    if request.method == 'POST':
        file = request.FILES['file']
        if not file.name.endswith('.xlsx') and not file.name.endswith('.xls'):
            messages.warning(
                request, 'Sai định dạng file, chỉ chấp nhận file excel có đuôi .xlsx hoặc .xls')
            return redirect('income')
        df = pd.read_excel(file)
        try:
            for i in range(len(df)):
                expenses = Expenses(user=request.user, amount=Decimal(float(
                    df['amount'][i])), date=df['date'][i], source=df['source'][i], description=df['description'][i])
                expenses.save()
        except:
            messages.warning(
                request, 'Kiểm tra lại định dạng file excel, có thể có lỗi trong quá trình import dữ liệu. Vui lòng đọc lại file hướng dẫn')
            return redirect('upgrade_success')
        messages.success(request, 'Import thành công')
        return redirect('expenses')
    return redirect('expenses')