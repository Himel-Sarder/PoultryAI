from django import forms
from .models import FarmProfile


class FarmProfileForm(forms.ModelForm):
    class Meta:
        model = FarmProfile
        fields = ['farm_name', 'location', 'farm_image', 'contact_number', 'description']
        widgets = {
            'farm_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm Location'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your farm...'}),
        }
