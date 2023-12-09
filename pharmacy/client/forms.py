from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client, Cart, CartItem, Order
from main.models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['age', 'address', 'phone']




class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pharmacy']