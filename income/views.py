from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Income
import json
from django.contrib import messages
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.staticfiles.storage import staticfiles_storage
import io
import pandas as pd
from decimal import Decimal

font_path = ('static/fonts/DejaVuSans/DejaVuSans.ttf')
pdfmetrics.registerFont(TTFont('DejaVu', font_path))


def index(request):
    return render(request, 'income_table.htmL')


def chart(request):
    return render(request, 'income_chart.html')


def get_chart_data(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        date = data.get('date')
        if date is None:
            return JsonResponse({'error': 'Missing date parameter'}, status=400)
        # Get the income data for the user and date provided by format mm/yyyy
        income = Income.objects.filter(user=user, date__month=date.split(
            '/')[0], date__year=date.split('/')[1])
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
        if sum(income_data) == 0:
            messages.success(request, "Chưa có dữ liệu thu nhập cho tháng này")
            return render(request, 'income_chart.html')
        return JsonResponse(income_data, safe=False)

def create_pdf(request):
    user = request.user
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    incomes = Income.objects.filter(user=user)
    SourceLable = ['Lương', 'Kinh doanh', 'Phụ thu nhập', 'Khác']
    p.setFont('DejaVu', 12)
    #i want to create a table for the incomes
    p.drawString(100, 750, f"Báo cáo Thu nhập cá nhân {user.username}")
    p.drawString(100, 730, "--------------------------------------------")
    p.drawString(100, 710, "Ngày")
    p.drawString(200, 710, "Loại")
    p.drawString(300, 710, "Chú thích")
    p.drawString(400, 710, "Tiền")
    y = 690
    for income in incomes:
        if y < 40:
            p.showPage()
            p.setFont('DejaVu', 12)
            p.drawString(100, 750, f"Báo cáo Thu nhập cá nhân {user.username}")
            p.drawString(100, 730, "--------------------------------------------")
            p.drawString(100, 710, "Ngày")
            p.drawString(200, 710, "Loại")
            p.drawString(300, 710, "Chú thích")
            p.drawString(400, 710, "Tiền")
            y = 690
        p.drawString(100, y, str(income.date))
        p.drawString(200, y, SourceLable[int(income.source)])
        p.drawString(300, y, income.description)
        p.drawString(400, y, str(income.amount))
        y -= 20 

    # Close the PDF object cleanly, and end writing process.
    p.save()
    p.showPage()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    return FileResponse(io.BytesIO(pdf), as_attachment=True, filename='incomes.pdf')

def import_excel(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if not file.name.endswith('.xlsx') and not file.name.endswith('.xls'):
            messages.warning(request, 'Sai định dạng file, chỉ chấp nhận file excel có đuôi .xlsx hoặc .xls')
            return redirect('income')
        df = pd.read_excel(file)
        for i in range(len(df)):
            income = Income(user=request.user, amount=Decimal(float(df['amount'][i])), date=df['date'][i], source=df['source'][i], description=df['description'][i])
            income.save()
        # except:
        #     messages.warning(request, 'Kiểm tra lại định dạng file excel, có thể có lỗi trong quá trình import dữ liệu')
        #     return redirect('income')
        messages.success(request, 'Import thành công')
        return redirect('income')
    return redirect('income')