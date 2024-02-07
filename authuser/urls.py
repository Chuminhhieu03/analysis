from django.urls import path
from authuser import views

urlpatterns = [
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('reset/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='reset'),
]
