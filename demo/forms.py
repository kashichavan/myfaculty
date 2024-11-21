from django import forms

class FacultyCreationForm(forms.Form):
    name = forms.CharField(max_length=100, label="Faculty Name")
    email = forms.EmailField(label="Faculty Email")
    phone_number = forms.CharField(max_length=15, required=False, label="Phone Number")
