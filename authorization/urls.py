from django.urls import path
from . import views

urlpatterns = [
    path('', views.handlelogin, name = 'login'),
    path('logout/', views.handlelogout, name = 'logout'),
]
