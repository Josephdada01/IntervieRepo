from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    """A class that define the Doctors model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        """returning the string representation"""
        return self.name


class Patient(models.Model):
    """A class that defines the Patient"""
    user = models.OnToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        """returnin the string representation of Patient"""
        return self.name
    

class Appointment(models.Model):
    """A class for the appointment"""
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)  # Duration of the appointment in minutes
    notes = models.TextField(blank=True, null=True)  # Additional notes for the appointment
    is_confirmed = models.BooleanField(default=False)  # Whether the appointment is confirmed
    is_completed = models.BooleanField(default=False)  # Whether the appointment is completed
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the appointment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the appointment was last updated

