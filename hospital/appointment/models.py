from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from appointment.managers import User
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=10, default="")
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, default="")
    description = models.TextField(max_length=1000, default="", help_text="Enter a brief description of the doctor")


    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('doctor-detail', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(max_length=1000, default="", help_text="Enter a brief description of the patient")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='patients')

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('doctor-detail', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()

"""
class Doctor(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the doctor")


    def get_absolute_url(self):
        Returns the URL to access a detail record for this book.
        return reverse('doctor-detail', args=[str(self.id)])
    

    def __str__(self):
        return self.title
    

class DoctorInstance(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    
    AVAILABILITY_STATUS = (
        ('b', 'Booked'),
        ('a', 'Available')
    )

    status = models.CharField(
        max_length=1,
        choices=AVAILABILITY_STATUS,
        blank=True,
        default='a',
        help_text='Appointment availability',
    )

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    desc = models.CharField(max_length=300)

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time}"

"""