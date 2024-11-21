from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.faculty_login, name='faculty_login'),  # Faculty Login
    path('logout/', views.faculty_logout, name='faculty_logout'),  # Faculty Logout
    path('batches/', views.faculty_batch_view, name='faculty_batches'),  # View faculty's batches
    path('add-attendance/<int:batch_id>/', views.add_attendance_view, name='add_attendance'),  # Add attendance for a batch
]
