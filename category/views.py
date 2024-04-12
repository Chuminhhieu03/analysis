from django.core.paginator import Paginator
from .services.CategoryService_Home import HomeCategory_Service
from .services.CategoryService_CRUD import CategoryAdd_Service, EditCategory_Service, DeleteCategory_Service

# Create your views here.
def index(request):
    return HomeCategory_Service(request)

def add(request):
    return CategoryAdd_Service(request)

def edit(request, id):
    return EditCategory_Service(request, id)

def delete(request, id):
    return DeleteCategory_Service(request, id)
