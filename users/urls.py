# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rentee_dashboard/', views.rentee_dashboard, name='rentee_dashboard'),
    
]
