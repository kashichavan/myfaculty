from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .models import Faculty
from .forms import FacultyCreationForm
import random
import string
from django.db import IntegrityError

def generate_random_password(length=8):
    """Generate a random password for faculty."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))

def admin_create_faculty_view(request):
    """Admin view to create a new faculty and send credentials."""
    if not request.user.is_staff:  # Ensure only admins can access
        return redirect('login')  # Redirect unauthorized users to login

    if request.method == 'POST':
        form = FacultyCreationForm(request.POST)
        if form.is_valid():
            # Extract faculty data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            # Generate a random password
            password = generate_random_password()

            try:
                # Create a user
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()

                # Create a faculty profile linked to the user
                faculty = Faculty.objects.create(
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    user=user
                )

                # Send an email to the faculty with credentials
                send_mail(
                    subject="Your Faculty Account Created",
                    message=f"Hello {name},\n\nYour faculty account has been created.\n\n"
                            f"Login Credentials:\n"
                            f"Username: {email}\n"
                            f"Password: {password}\n\n"
                            f"Please change your password after logging in.\n\n"
                            f"Thank you!",
                    from_email="admin@example.com",  # Replace with your admin email
                    recipient_list=[email],
                )

                messages.success(request, f"Faculty {name} created and credentials sent to {email}.")
                return redirect('demo:faculty_login')  # Replace with the admin dashboard URL

            except IntegrityError:
                # Handle case where email/username already exists
                messages.error(request, f"A user with the email {email} already exists.")
                return redirect('admin_create_faculty')  # Stay on the same page for reattempt

    else:
        form = FacultyCreationForm()

    return render(request, 'admin_create_faculty.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Batch, Attendance

# Faculty Login View
def faculty_login(request):
    """Faculty can log in to the application."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('faculty_batches')  # Redirect to batches view once logged in
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'faculty_login.html')


# Faculty Logout View
@login_required
def faculty_logout(request):
    """Log out the faculty."""
    logout(request)
    return redirect('faculty_login')  # Redirect to login page after logout


# Faculty view to see their batches
@login_required
def faculty_batch_view(request):
    """Faculty can view all batches assigned to them."""
    if request.user.is_staff:  # Ensure the user is not an admin
        return redirect('admin_dashboard')  # Redirect to admin dashboard if user is admin
    
    # Get the batches assigned to the faculty
    batches = Batch.objects.filter(faculty=request.user.faculty_profile)

    return render(request, 'faculty_batches.html', {'batches': batches})


# Add Attendance view
@login_required
def add_attendance_view(request, batch_id):
    """Faculty can add attendance for a specific batch."""
    try:
        batch = Batch.objects.get(id=batch_id)
    except Batch.DoesNotExist:
        raise Http404("Batch not found")

    if batch.faculty.user != request.user:  # Ensure only the faculty assigned to the batch can add attendance
        return redirect('faculty_batches')  # Redirect if the faculty is not assigned to the batch

    if request.method == 'POST':
        # Process form submission to add attendance
        student_count = request.POST.get('student_count')
        if student_count.isdigit():  # Ensure the input is a number
            attendance = Attendance(batch=batch, faculty=request.user.faculty_profile,
                                     student_count=int(student_count), date=request.POST.get('date'),
                                     time=request.POST.get('time'))
            attendance.save()
            return redirect('faculty_batches')  # Redirect to the batches view after saving attendance

    return render(request, 'add_attendance.html', {'batch': batch})
