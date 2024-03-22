
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class DoctorSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user

class PatientSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = False
        if commit:
            user.save()
        return user
