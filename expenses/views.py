from .services.ExpenseService_Home import ExpenseHome_Service
from .services.ExpenseService_Chart import ExpenseChart_Service, ExpenseDataChar_Service
from .services.ExpenseService_CRUD import ExpenseAdd_Service, ExpenseDelete_Service, ExpenseEdit_Service
from .services.ExpenseService_Export import ExpenseExport_Service
from .services.ExpenseService_Import import ExpenseImport_Service


def index(request):
    return ExpenseHome_Service(request)

def chart(request):
    return ExpenseChart_Service(request)

def get_chart_data(request):
    return ExpenseDataChar_Service(request)

def create_pdf(request):
    return ExpenseExport_Service(request)

def import_excel(request):
    return ExpenseImport_Service(request)

def add(request):
    return ExpenseAdd_Service(request)

def edit(request, id):
    return ExpenseEdit_Service(request, id)

def delete(request, id):
    return ExpenseDelete_Service(request, id)
