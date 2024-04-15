from django.shortcuts import render, redirect
from appointment.managers import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index(request):
    """index function"""
    return render(request, 'index.html')


def doctor_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        custom_id = request.POST.get('custom_id')

        if custom_id != "Doctor":
            messages.error(request, "You are not our staff yet")  
            return render(request, 'doctor_signup.html')

        # Check if the user with the provided email already exists
        if User.objects.filter(email=email).exists():
            messages.info(request, "An account with this email already exists. Please log in.")
            return render(request, 'doctor_signup.html')

        # Create the user
        user = User.objects.create_user(email=email, username=username, password=password, custom_id=custom_id)
        if user:
            user.is_active = True
            user.save()
            messages.success(request, "Account created and logged in successfully")
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "Failed to create an account. Please try again.")
            return render(request, "doctor_signup.html")

    return render(request, 'doctor_signup.html')



def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')
