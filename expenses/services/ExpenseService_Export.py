from django.shortcuts import redirect
from ..models import Expenses
from django.contrib import messages
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from pathlib import Path
from expenses.constVar import SOURCE_USER_ARR, SOURCE_BUSINESS_ARR

THIS_FOLDER = Path(__file__).parent.resolve()
ROOT_FOLDER = THIS_FOLDER.parent.parent
font_path = str(ROOT_FOLDER / 'static' /'fonts'/'DejaVuSans'/ 'DejaVuSans.ttf')

pdfmetrics.registerFont(TTFont('DejaVu', font_path))

def ExpenseExport_Service(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.upgrade == False:
        messages.warning(request, "Bạn chưa nâng cấp tài khoản")
        return redirect('upgrade')
    user = request.user
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    expensess = Expenses.objects.filter(user=user)
    # convert amount to int and have a comma every 3 numbers
    for expenses in expensess:
        expenses.amount = '{:,}'.format(int(expenses.amount))
    SourceLable = SOURCE_USER_ARR if user.userprofile.type == "0" else SOURCE_BUSINESS_ARR
    p.setFont('DejaVu', 12)
    # i want to create a table for the expensess
    if user.userprofile.type == "1":
        p.drawString(100, 750, f"Báo cáo Chi tiêu doanh nghiệp {user.username}")
    else: 
        p.drawString(100, 750, f"Báo cáo Chi tiêu cá nhân {user.username}")
    p.drawString(100, 730, "--------------------------------------------")
    p.drawString(100, 710, "Ngày")
    p.drawString(200, 710, "Loại")
    p.drawString(300, 710, "Chú thích")
    p.drawString(400, 710, "Tiền")
    y = 690
    for expenses in expensess:
        if y < 40:
            p.showPage()
            p.setFont('DejaVu', 12)
            if user.userprofile.type == "1":
                p.drawString(100, 750, f"Báo cáo Chi tiêu doanh nghiệp {user.username}")
            else: 
                p.drawString(100, 750, f"Báo cáo Chi tiêu cá nhân {user.username}")
            p.drawString(
                100, 730, "--------------------------------------------")
            p.drawString(100, 710, "Ngày")
            p.drawString(200, 710, "Loại")
            p.drawString(300, 710, "Chú thích")
            p.drawString(400, 710, "Tiền")
            y = 690
        p.drawString(100, y, str(expenses.date))
        p.drawString(200, y, SourceLable[int(expenses.source)])
        p.drawString(300, y, expenses.description)
        p.drawString(400, y, str(expenses.amount) + " VNĐ")
        y -= 20

    # Close the PDF object cleanly, and end writing process.
    p.save()
    p.showPage()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    messages.success(request, 'Tạo báo cáo chi tiêu thành công')
    return FileResponse(io.BytesIO(pdf), as_attachment=True, filename='expensess.pdf')