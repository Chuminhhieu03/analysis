from django.urls import path
from authuser import views

urlpatterns = [
    path('', views.index, name='index'),
]
