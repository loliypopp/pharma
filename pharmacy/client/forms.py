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
        labels = {
            'first_name':'Имя: ',
            'last_name':'Фамилия: ',
            'password1': 'Пароль: ',
            'password2': 'Подтверждение: '
        }

class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['age', 'address', 'phone']
        labels = {
            'age':'Возраст: ',
            'address':'Адрес: ',
            'phone': 'Номер телефона: ',
        }




class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pharmacy']
        labels = {
            'pharmacy': 'Аптека:',
        }