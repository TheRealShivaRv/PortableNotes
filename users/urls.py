from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logoutapp/', views.logoutapp, name='logoutapp'),
    path('signup/', views.signup, name='signup'),
    path('resetpwd/', views.resetpwd, name='resetpwd'),
    path('passwordreset/', views.passwordreset, name='passwordreset'),
    path('pwdresetverification/', views.pwdresetverification, name='pwdresetverification'),
    path('verification/', views.verification, name='verification'),
    path('settings/', views.settings, name='settings'),
    path('deleteuser/', views.deleteuser, name='deleteuser')
]
