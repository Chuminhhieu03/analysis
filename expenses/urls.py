from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.index, name='expenses'),
]



