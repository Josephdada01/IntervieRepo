from django.urls import path
from .views import DoctorAPIView, PatientAPIView, AppointmentAPIView, login_view

"""The urls path for the doctors, patients and the apointments"""
urlpatterns = [
    path('doctors/', DoctorAPIView.as_view(), name='doctor-list-create'),
    path('patients/', PatientAPIView.as_view(), name='patient-list-create'),
    path('appointments/', AppointmentAPIView.as_view(), name='appointment-list-create'),
    path('login/', login_view, name='login'),
]
