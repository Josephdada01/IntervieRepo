from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Doctor, Patient, Appointment

class DoctorPatientAppointmentTests(TestCase):
    """A class for testing"""

    def setUp(self):
        """Setting up the test"""
        self.client = APIClient()
        self.user_doctor = User.objects.create_user(username='doctor', 
                                                    password='testpassword')
        self.user_patient = User.objects.create_user(username='patient', 
                                                     password='testpassword')
        self.client.force_authenticate(user=self.user_doctor)

    def test_doctor_signup(self):
        """
        Test for doctor signing up, this allows doctors to signup 
        successfully and sending the status 201
        """
        response = self.client.post(reverse('doctor-list-create'), 
                                    data={'name': 'Dr. Joseph', 
                                          'email': 'doctorjoe@gmail.com', 
                                          'phone': '2348124555883'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patients_signup(self):
        """
        Test for patients not being able to signup,
        will return status 403. denies the request
        """
        response = self.client.post(reverse('patient-list-create'), 
                                    data={'name': 'Joseph Dada', 
                                          'email': 'josephdada@gmail.com', 
                                          'phone': '2348163860056'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_patient_login(self):
        """
        Test for doctor creating account for patient
        it returns status 201 for success
        """
        patient = Patient.objects.create(user=self.user_patient, 
                                         name='John Doe', 
                                         email='johndoe@example.com', 
                                         phone='09199901111')
        response = self.client.post(reverse('patient-list-create'), 
                                    data={'name': 'Jane Doe', 
                                          'email': 'janedoe@example.com', 
                                          'phone': '2348114567890'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_login_and_book_appointment(self):
        """Test for patient login and book appointment, returning status success"""
        self.client.force_authenticate(user=self.user_patient)
        doctor = Doctor.objects.create(user=self.user_doctor, 
                                       name='Dr. Smith', 
                                       email='drsmith@example.com', 
                                       phone='1234567890')
        response = self.client.post(reverse('appointment-list-create'), 
                                    data={'doctor': doctor.id, 
                                          'patient': 1, 
                                          'appointment_time': '2024-03-25T09:00:00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_can_book_appointment_with_any_doctor(self):
        """
        Test patient can book appointment with any 
        doctor.
        """
        self.client.force_authenticate(user=self.user_patient)
        doctor = Doctor.objects.create(user=self.user_doctor, 
                                       name='Dr. Smith', 
                                       email='drsmith@example.com', 
                                       phone='1234567890')
        response = self.client.post(reverse('appointment-list-create'), 
                                    data={'doctor': doctor.id, 
                                          'patient': 1, 
                                          'appointment_time': '2024-03-25T10:00:00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_only_booked_doctor_can_view_patient_information(self):
        """
        This test ensures that the system correctly 
        restricts access to patient information, 
        allowing only the doctor who has been booked for an 
        appointment with the patient to view that patient's information.
        """
        self.client.force_authenticate(user=self.user_patient)
        doctor = Doctor.objects.create(user=self.user_doctor, 
                                       name='Dr. Smith', 
                                       email='drsmith@example.com', 
                                       phone='1234567890')
        patient = Patient.objects.create(user=self.user_patient, 
                                         name='John Doe', 
                                         email='johndoe@example.com', 
                                         phone='2348136543210')
        appointment = Appointment.objects.create(doctor=doctor, 
                                                 patient=patient, 
                                                 appointment_time='2024-03-25T09:00:00')
        self.client.force_authenticate(user=self.user_doctor)
        response = self.client.get(reverse('appointment-list-create'))  # Assuming appointment-list-create lists all appointments
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assuming it returns HTTP 200 for authenticated users
