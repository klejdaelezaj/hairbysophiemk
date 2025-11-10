
from django import forms
from .models import Appointment

SERVICE_CHOICES = [
    ('haircut', 'Haircut'),
    ('coloring', 'Hair Coloring'),
    ('styling', 'Hair Styling'),
]


class AppointmentForm(forms.ModelForm):
    service = forms.ChoiceField(choices=SERVICE_CHOICES)

    class Meta:
        model = Appointment
        fields = ['name', 'email', 'date', 'time', 'service']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
