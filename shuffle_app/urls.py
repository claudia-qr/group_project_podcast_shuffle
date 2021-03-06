from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('account/<int:id>', views.account),
    path('home', views.home),
    path('editaccount', views.editaccount),
    path('editpw', views.editpw),
    path('library', views.library),
    path('logout', views.logout),
]