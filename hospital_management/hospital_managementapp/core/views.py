from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .forms import DoctorSignUpForm, PatientSignUpForm
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from core.serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer
from .models import Doctor, Patient, Appointment

class DoctorSignUpAPIView(APIView):
    """
    API endpoint for doctor signup
    """
    def post(self, request):
        form = DoctorSignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientSignUpAPIView(APIView):
    """
    API endpoint for patient signup
    """
    def post(self, request):
        form = PatientSignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorAPIView(generics.ListCreateAPIView):
    """
    API endpoint to list and create doctors
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientAPIView(generics.ListCreateAPIView):
    """
    API endpoint to list and create patients
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentAPIView(generics.ListCreateAPIView):
    """
    API endpoint to list and create appointments
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.is_doctor:
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
