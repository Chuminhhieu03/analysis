from django.urls import path
from authuser import views

urlpatterns = [
    path('', views.index, name='index'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('upgrade', views.upgrade, name='upgrade'),
]
