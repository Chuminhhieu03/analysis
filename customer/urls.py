from django.urls import path
from customer import views

urlpatterns = [
    path('', views.index, name='customer'),
    path('add', views.add, name='add_customer'),
    path('edit/<int:id>', views.edit, name='edit_customer'),
    path('delete/<int:id>', views.delete, name='delete_customer'),
]