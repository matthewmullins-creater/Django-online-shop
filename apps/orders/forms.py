from django import forms
from .models import Order,PaymentType

# Chice_PaymentType=((1,"Payment through banking gateway"),(2,"Payment on delivery"))
class OrderForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        }),
        error_messages={
            'required': 'This field cannot be empty'
        },

        
    )
    
    family = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Family Name'
        }),
        error_messages={
            'required': 'This field cannot be empty'
        },

    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        required=False
    )
    
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        }),
        required=False
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address',
            "rows": "2",

        }),
        error_messages={
            'required': 'This field cannot be empty'
        }
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Description',
            "rows": "4"
        }),
        required=False
    )
    
    payment = forms.ModelChoiceField(
        queryset=PaymentType.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None
    )
