from django.urls import path
from product import views

urlpatterns = [
    path('', views.index, name='product'),
    path('add', views.add, name='add_product'),
    path('edit/<int:id>', views.edit, name='edit_product'),
    path('delete/<int:id>', views.delete, name='delete_product'),
]