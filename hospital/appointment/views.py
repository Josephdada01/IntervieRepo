from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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

        # Check if the custom_id is "Doctor"
        if custom_id != "Doctor":
            messages.error(request, "You are not authorized to sign up as a doctor.")
            return render(request, 'doctor_signup.html')

        # Check if the user with the provided email already exists
        if User.objects.filter(email=email).exists():
            messages.info(request, "An account with this email already exists. Please log in.")
            return render(request, 'doctor_signup.html')

        # Create the user
        user = User.objects.create_user(email=email, username=username, password=password)
        if user:
            user.is_active = True
            user.save()
            messages.success(request, "Account created and logged in successfully")
            # Log in the user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                messages.error(request, "Failed to log in. Please try again.")
                return redirect('login')  # Redirect to the login page if login fails
        else:
            messages.error(request, "Failed to create an account. Please try again.")
            return render(request, "doctor_signup.html")

    return render(request, 'doctor_signup.html')

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, log them in
            # login(request, user)
            messages.success(request, " successful!")
            return redirect('doctor_dashboard')  # Redirect to dashboard upon successful login
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password")
            return render(request, 'doctor_login.html')  # Render login page with error message

    return render(request, 'doctor_login.html')

"""
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
"""

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')
