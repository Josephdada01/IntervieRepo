from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from appointment.models import Doctor, Appointment
from math import ceil
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404




# Create your views here.
def index(request):
    """index function"""
    return render(request, 'index.html')

"""
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
            #user.is_doctor = True
            user.save()
            messages.success(request, "Account created and logged in successfully")
            # Log in the user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                messages.error(request, "Failed to log in. Please try again.")
                return redirect('doctor_login.html')  # Redirect to the login page if login fails
        else:
            messages.error(request, "Failed to create an account. Please try again.")
            return render(request, "doctor_signup.html")

    return render(request, 'doctor_signup.html')
"""

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            messages.success(request, " successful!")
            return redirect('doctor_dashboard')  # Redirect to dashboard upon successful login
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password")
            return render(request, 'doctor_login.html')  # Render login page with error message

    return render(request, 'doctor_login.html')

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
            #user.is_doctor = True
            user.save()

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('doctor_login')  # Redirect to the login page
        else:
            messages.error(request, "Failed to create an account. Please try again.")
            return render(request, "doctor_signup.html")

    return render(request, 'doctor_signup.html')


@login_required
def register_patient(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "This username or email is already taken.")
            return render(request, 'register_patient.html')

        # Create the patient account
        user = User.objects.create_user(email=email, username=username, password=password)
        #user.is_patient = True  # Mark the user as a patient
        user.is_active = True
        user.save()

        messages.success(request, "Patient account created successfully.")
        return redirect('doctor_dashboard')  # Redirect to the dashboard or any other page

    return render(request, 'register_patient.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None: #and user.is_patient:
            # Login the user
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('patient_dashboard')  # Redirect to the patient dashboard or any other page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'patient_login.html')


@login_required
def doctor_dashboard(request):
    if request.user.is_authenticated: #and user.is_patient:
        return render(request, 'doctor_dashboard.html')
    else:
        # Redirect or show an error message if the user is not authenticated or not a doctor
        # You can customize this based on your application's requirements
        messages.warning(request, "Login & Try Again")
        return redirect('/doctor_login.html')


@login_required
def patient_dashboard(request):
    if request.user.is_authenticated: #and request.user.is_patient:
        alldoctors = []
        catdoctors = Doctor.objects.values('category')
        cats = {item['category'] for item in catdoctors}
        for cat in cats:
            doc = Doctor.objects.filter(category=cat)
            n = len(doc)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            alldoctors.append([doc, range(1, nSlides), nSlides])

        params = {'alldoctors': alldoctors}  # Parameters to be passed to the template
        return render(request, 'patient_dashboard.html', params)
    else:
        # Redirect or show an error message if the user is not authenticated or not a doctor
        messages.warning(request, "Login & Try Again")


def schedule_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)  # Ensure doctor exists
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor  # Assign the doctor
            appointment.patient = request.user.patient  # Assign the patient
            appointment.save()
            return redirect('appointment_confirmation')  # Redirect to a confirmation page
    else:
        # Pre-fill the form with doctor and patient information
        form = AppointmentForm(initial={'doctor': doctor, 'patient': request.user.patient})
    
    return render(request, 'schedule_appointment.html', {'form': form, 'doctor': doctor})

def appointment_confirmation(request):
    return (request, 'appointment_confirmation')

"""
def schedule_appointment(request, doctor_id):

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient  # Assuming patient is the currently logged-in user
            appointment.save()
            return redirect('appointment_confirmation')  # Redirect to a confirmation page
    else:
        # Pre-fill the form with doctor and patient information
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        form = AppointmentForm(initial={'doctor': doctor, 'patient': request.user.patient})
    
    return render(request, 'schedule_appointment.html', {'form': form})




"""
"""

@login_required
def patient_dashboard(request):
    if request.user.is_authenticated: #and request.user.is_patient:
        alldoctors = []
        catdoctors = Doctor.objects.values('category')
        cats = {item['category'] for item in catdoctors}
        for cat in cats:
            doc = Doctor.objects.filter(category=cat)
            n = len(doc)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            alldoctors.append([doc, range(1, nSlides), nSlides])

        params = {'allprods': alldoctors}  # Parameters to be passed to the template
        return render(request, 'patient_dashboard.html', params=params)
    else:
        # Redirect or show an error message if the user is not authenticated or not a doctor
        messages.warning(request, "Login & Try Again")


        # Logic to retrieve products and organize them for display
    
        return redirect('/patient_login.html')
"""