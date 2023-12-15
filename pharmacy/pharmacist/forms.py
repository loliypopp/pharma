from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pharmacist, Medicine
from main.models import CustomUser
from client.models import Order
from courier.models import Courier

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


class FreeCourierOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courier']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор курьеров только теми, у которых статус 'Свободен'
        free_couriers = Courier.objects.filter(status='Свободен')
        self.fields['courier'].queryset = free_couriers