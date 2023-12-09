from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pharmacist, Medicine
from main.models import CustomUser
from client.models import Order

class CustomUserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

class PharmacistRegistrationForm(forms.ModelForm):
    class Meta:
        model = Pharmacist
        fields = ['expirience', 'license_number', 'pharmacy']


class MedicineAdditionForm(forms.ModelForm):
    class Meta:
        model = Medicine
        exclude = ['slug']


