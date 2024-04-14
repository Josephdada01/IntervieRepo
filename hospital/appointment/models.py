from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Create your models here.
"""
  Doctor Model
    - first name
    - last name
    - is_picked (boolean, default=false)

  Patient model -> Django Abstract Base User:
    - first name
    - last name
    - phone
    - email
    - id

  Appointment Model:
    - date
    - doctor's id -> ForeignKey(Doctor)
    - patient's id -> ForeignKey(Patient)
"""
class Doctor(AbstractUser):
    """Doctor class"""
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    AVAILABILITY_STATUS = (
        ('b', 'booked'),
        ('a', 'Available')
    )

    status = models.CharField(
        max_length=1,
        choices=AVAILABILITY_STATUS,
        blank=True,
        default='a',
        help_text='appointment availability',
    )

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
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

