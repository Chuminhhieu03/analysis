from .services.ProductService_Home import ProductHome_Service
from .services.ProductService_CRUD import AddProduct_Service, EditProduct_Service, DeleteProduct_Service

# Create your views here.
def index(request):
    return ProductHome_Service(request)

def add(request):
    return AddProduct_Service(request)

def edit(request, id):
    return EditProduct_Service(request)

def delete(request, id):
    return DeleteProduct_Service(request)