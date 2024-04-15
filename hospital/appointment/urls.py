from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('doctor_signup', views.doctor_signup, name="doctor_signup"),
    path('doctor_dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('login_view/', views.login_view, name='login'),
]