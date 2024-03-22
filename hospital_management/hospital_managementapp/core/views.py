from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, Patient, Appointment
from core.serialiazers import DoctorSerializer, PatientSerializer, AppointmentSerializer

class DoctorAPIView(generics.ListCreateAPIView):
    """
    Specifies the model to serialize 
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientAPIView(generics.ListCreateAPIView):
    """
    Specifies the model to serialize 
    Specifies that all fields of the Patient
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentAPIView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    """
    Specifies the model to serialize 
    Specifies that all fields of the Apointment 
    only authenticated user can access the view
    """
    permission_classes = [IsAuthenticated]
