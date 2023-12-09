from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.views.generic import CreateView, ListView, DetailView, DeleteView, TemplateView
from .forms import CustomUserRegistrationForm, PharmacistRegistrationForm, MedicineAdditionForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from client.models import Order, OrderItem, Client



class TheStartPage(ListView):
    model = Medicine
    template_name = 'pharmacist/start_page.html'
    context_object_name = 'medicines'



class CreateMedicineView(CreateView):
    model = Medicine
    template_name = 'pharmacist/add_medicine.html'
    form_class = MedicineAdditionForm
    



def register_pharmacist(request):
    if request.method == 'POST':
        user_form = CustomUserRegistrationForm(request.POST)
        pharmacist_form = PharmacistRegistrationForm(request.POST)
        
        if user_form.is_valid() and pharmacist_form.is_valid():
            user = user_form.save()
            pharmacist = pharmacist_form.save(commit=False)
            pharmacist.user = user
            pharmacist.save()
            
            login(request, user)
            return redirect('start_page_pharmacist')
    else:
        user_form = CustomUserRegistrationForm()
        pharmacist_form = PharmacistRegistrationForm()



    return render(request, 'pharmacist/registration.html', {'user_form': user_form, 'pharmacist_form': pharmacist_form})


def logout_pharmacist(request):
    logout(request)
    return redirect('start_page_pharmacist')


class LoginPageView(LoginView):
    template_name = 'pharmacist/login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('start_page_pharmacist')



class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'pharmacist/medicine_detail.html'
    slug_param = 'slug'
    slug_url_kwarg = 'slug'



class UserProfileView(TemplateView):
    template_name = 'pharmacist/profile.html'



def orders_handling(request):
    pharmacist = get_object_or_404(Pharmacist, user=request.user)
    orders = Order.objects.filter(pharmacy = pharmacist.pharmacy)

    context = {'orders': orders}
    return render(request, 'pharmacist/order_handling.html', context)



def order_details(request, link):
    link = int(link)
    order = get_object_or_404(Order, id=link)

    order.status = 'Сбор'
    order.save()
    
    client = order.user

    order_items = OrderItem.objects.filter(order=link)
    context = {'order':order,
               'orders':order_items}
    
    return render(request, 'pharmacist/order_details.html', context)