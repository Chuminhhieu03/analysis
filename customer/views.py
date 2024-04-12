from .services.CustomerService_Home import HomeCustomer_Service
from .services.CustomerService_CRUD import AddCustomer_Service, EditCustomer_Service, DeleteCustomer_Service

# Create your views here.
def index(request):
    return HomeCustomer_Service(request)

def add(request):
    return AddCustomer_Service(request)

def edit(request, id):
    return EditCustomer_Service(request, id)

def delete(request, id):
    return DeleteCustomer_Service(request, id)