from django.shortcuts import get_object_or_404, render
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from pharmacist.models import Medicine
from django.views.generic import CreateView, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import resolve, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from pharmacist.forms import CustomUserRegistrationForm
from client.models import Order, OrderItem, Client


def TheStartPage(request):
    try:
        courier = get_object_or_404(Courier, user=request.user)
        orders = Order.objects.filter(courier=courier).exclude(status='Поиск курьера')
        context = {
            'orders' : orders
        }
    except:
        logout(request)
        return redirect('registration_c')

    return render(request, 'courier/start_page.html', context)


def register_courier(request):
    if request.method == 'POST':
        user_form = CustomUserRegistrationForm(request.POST)
        courier_form = CourierRegistrationForm(request.POST)
        
        if user_form.is_valid() and courier_form.is_valid():
            user = user_form.save()
            courier = courier_form.save(commit=False)
            courier.user = user
            courier.save()
            
            login(request, user)
            return redirect('start_page_c')
    else:
        user_form = CustomUserRegistrationForm()
        courier_form = CourierRegistrationForm()



    return render(request, 'courier/registration.html', {'user_form': user_form, 'courier_form': courier_form})



def logout_courier(request):
    logout(request)
    return redirect('start_page_c')


class LoginPageView(LoginView):
    template_name = 'courier/login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('start_page_c')


class UserProfileView(TemplateView):
    template_name = 'courier/profile.html'



def order_details(request, link):
    order_items = OrderItem.objects.filter(order=link)
    order = Order.objects.get(id=link)
    courier = Courier.objects.get(user=request.user)
    if request.method == 'POST':
        order.status = 'Доставлен'
        order.save()
        courier.status = 'Свободен'
        courier.save()
        return redirect('start_page_c')
    client = order.user
    context ={
        'orders':order_items,
        'user':client,
        'ord':order
        }
    
    return render(request, 'courier/order_details.html', context)


def decline_delivery(request, link):
    order = Order.objects.get(id=link)
    order.status = 'Поиск курьера'
    order.save()

    return redirect('start_page_c')