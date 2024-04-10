from django.urls import path
from category import views

urlpatterns = [
    path('', views.index, name='category'),
    path('add', views.add, name='add_category'),
    path('edit/<int:id>', views.edit, name='edit_category'),
    path('delete/<int:id>', views.delete, name='delete_category'),
]