from django.contrib import admin
from django.contrib.admin.decorators import register
# Register your models here.
from .models import Faculty,Room,Slot,Subject,Batch,Attendance

@register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

@register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_number')

@register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('room', 'slot_time', 'batch', 'faculty')
@register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'faculty', 'subject') 

@register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('batch', 'faculty', 'subject', 'date', 'time', 'student_count')  # Added 'subject' as a method
    list_filter = ('date', 'faculty', 'batch')

    def subject(self, obj):
        return obj.batch.subject.name  # Access 'subject' via the related 'batch'

    subject.admin_order_field = 'batch__subject'  # Enable sorting by 'subject'
    subject.short_description = 'Subject'  # Label in the admin panel


