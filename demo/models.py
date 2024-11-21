from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile',null=True)
    #department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    #code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Batch(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='batches')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='batches')

    def __str__(self):
        return f"{self.name} ({self.subject.name})"
    
    def batch_number(self):
        return f"Batch-{self.id}"


class Room(models.Model):
    room_number = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.room_number

    @staticmethod
    def initialize_rooms():
        """Create rooms for 5 floors, 5 rooms per floor (101-505)."""
        for floor in range(1, 6):
            for room in range(1, 6):
                room_number = f"{floor}{room:02}"  # Format as 101, 102, ..., 505
                Room.objects.get_or_create(room_number=room_number)


class Slot(models.Model):
    SLOT_CHOICES = [
        ('1', 'Slot 1: 7:30 AM - 9:30 AM'),
        ('2', 'Slot 2: 10:00 AM - 12:00 AM'),
        ('3', 'Slot 3: 12:30 AM - 2:30 PM'),
        ('4', 'Slot 4: 3:00 PM - 5:00 PM'),
        ('5', 'Slot 5: 5:30 PM - 7:30 PM'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='slots')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='slots')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='slots')
    slot_time = models.CharField(max_length=1, choices=SLOT_CHOICES)

    class Meta:
        unique_together = ('room', 'slot_time')  # Prevent overlapping slots in the same room
        ordering = ['slot_time']

    def __str__(self):
        return f"{self.room.room_number} | Slot {self.slot_time} | {self.batch.name}"

    def clean(self):
        # Ensure no faculty is assigned to two batches in the same slot
        overlapping_slot = Slot.objects.filter(
            faculty=self.faculty,
            slot_time=self.slot_time
        ).exclude(id=self.id)
        if overlapping_slot.exists():
            raise ValidationError(f"Faculty {self.faculty.name} is already assigned to another batch in Slot {self.slot_time}.")

        # Ensure each room can only have 5 slots occupied
        if Slot.objects.filter(room=self.room).count() >= 5:
            raise ValidationError(f"Room {self.room.room_number} already has 5 slots allocated.")

class Attendance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='attendances')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()  # Attendance date
    time = models.TimeField()  # Attendance time
    student_count = models.PositiveIntegerField()  # Number of students who attended

    class Meta:
        unique_together = ('batch', 'date', 'time')  # Prevent duplicate attendance records

    def __str__(self):
        return f"Batch: {self.batch.name} | Faculty: {self.faculty.name} | Date: {self.date} | Students: {self.student_count}"