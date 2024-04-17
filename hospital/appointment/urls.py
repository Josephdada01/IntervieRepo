from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('doctor_signup', views.doctor_signup, name="doctor_signup"),
    path('doctor_dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('patient_dashboard', views.patient_dashboard, name="patient_dashboard"),
    path('doctor_login', views.doctor_login, name='doctor_login'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('patient_login/', views.patient_login, name='patient_login'),
    #path('schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('schedule_appointment/<uuid:doctor_id>/', views.schedule_appointment, name='schedule_appointment'),
    path('appointment_confirmation/', views.schedule_appointment, name='appointment_confirmation'),
]