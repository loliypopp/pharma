from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Courier
from main.models import CustomUser
from client.models import Order



class CourierRegistrationForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ['expirience']