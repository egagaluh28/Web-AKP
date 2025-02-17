# traffic/forms.py
from django import forms
from .models import TrafficData

class TrafficForm(forms.ModelForm):
    class Meta:
        model = TrafficData
        fields = ['location', 'density']