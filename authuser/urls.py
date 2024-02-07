from django.urls import path
from authuser import views

urlpatterns = [
    path('', views.index, name='profile_user'),
    path('/edit', views.edit_profile, name='edit_profile_user'),
    path('/feedback', views.feedback_user, name='feedback_user')
]
