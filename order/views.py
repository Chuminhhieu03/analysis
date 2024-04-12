from .services.OrderService_Home import HomeOrder_Service
from .services.OrderService_CRUD import AddOrder_Service, DetailOrder_Service, EditOrder_Service

# Create your views here.
def index(request):
    return HomeOrder_Service(request)
    
def add(request):
    return AddOrder_Service(request)

def detail(request, id):
    return DetailOrder_Service(request, id)

def edit(request, id):
    return EditOrder_Service(request, id)