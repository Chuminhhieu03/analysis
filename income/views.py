from .services.IncomeService_Home import IncomeHome_Service
from .services.IncomeService_Chart import IncomeChart_Service, IncomeDataChar_Service
from .services.IncomeService_CRUD import IncomeAdd_Service, IncomeDelete_Service, IncomeEdit_Service
from .services.IncomeService_Import import IncomeImport_Service
from .services.IncomeService_Export import IncomeExport_Service


def index(request):
    return IncomeHome_Service(request)

def chart(request):
    return IncomeChart_Service(request)

def get_chart_data(request):
    return IncomeDataChar_Service(request)

def create_pdf(request):
    return IncomeExport_Service(request)

def import_excel(request):
    return IncomeImport_Service(request)

def add(request):
    return IncomeAdd_Service(request)

def edit(request, id):
    return IncomeEdit_Service(request, id)

def delete(request, id):
    return IncomeDelete_Service(request, id)
