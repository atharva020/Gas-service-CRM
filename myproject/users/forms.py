from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import GasServiceRequest

class GasServiceRequestForm(forms.ModelForm):
    class Meta:
        model = GasServiceRequest
        fields = ['request_type', 'description']
        widgets = {
            'request_type': forms.Select(choices=[
                ('Connection', 'New Gas Connection'),
                ('Repair', 'Repair Service'),
                ('Maintenance', 'Maintenance'),
                ('Complaint', 'File Complaint')
            ]),
            'description': forms.Textarea(attrs={'rows': 4})
        }