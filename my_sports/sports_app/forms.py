# In forms.py

from django import forms
from .models import Enquiry, Register, Item_entry, KitItem


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['first_name', 'contact_no',]


class CoachAllocation:
    pass


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'mobile', 'email', 'address',   ]

        widgets = {

            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last_name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}),
        }

