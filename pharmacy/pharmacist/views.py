from client.models import Client, Order, OrderItem
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView)
from pyexpat.errors import messages

from .forms import (CustomUserRegistrationForm, FreeCourierOrderForm,
                    MedicineAdditionForm, PharmacistRegistrationForm)
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class TheStartPage(ListView):
    model = Medicine
    template_name = 'pharmacist/start_page.html'
    context_object_name = 'medicines'



class CreateMedicineView(CreateView):
    model = Medicine
    template_name = 'pharmacist/add_medicine.html'
    form_class = MedicineAdditionForm
    success_url = reverse_lazy('start_page_pharmacist')
    



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
    
    if request.method == 'POST':
        form = FreeCourierOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            courier = order.courier
            courier.status = 'Занят'
            courier.save()
            order.status = 'Доставляется'
            order.save()
            return redirect('orders_handling')
        
    else:
        # Если запрос не POST, создайте форму
        form = FreeCourierOrderForm(instance=order)

    client = order.user
    print(order)
    order_items = OrderItem.objects.filter(order=link)
    print(order_items)
    context = {'orderr':order,
               'orders':order_items,
               'form': form}
    
    return render(request, 'pharmacist/order_details.html', context)



def ph_meds(request):
    pharmacist = Pharmacist.objects.get(user=request.user)
    pharmacy = pharmacist.pharmacy.id
    print(pharmacy)
    meds = Medicine.objects.filter(pharmacies=pharmacy)
    context = {
        'meds':meds
    }
    return render(request, 'pharmacist/ph_meds.html', context)