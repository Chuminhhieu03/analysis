from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('income/', views.income, name='income'),
    path('expense/', views.expense, name='expense'),
    path('expense/add_info/',views.add_info,name = 'add_info'),
]



