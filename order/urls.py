from django.urls import path
from order import views

urlpatterns = [
    path('', views.index, name='order'),
    path('add/', views.add, name='add_order'),
    path('detail/<int:id>/', views.detail, name='detail_order'),
    path('edit/<int:id>/', views.edit, name='edit_order'),
    path('delete/<int:id>/', views.delete, name='delete_order'),
]