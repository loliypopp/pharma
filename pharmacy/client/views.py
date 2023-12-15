from django.shortcuts import get_object_or_404, render
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from .models import Medicine
from django.views.generic import CreateView, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import resolve, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

class TheStartPage(ListView):
    model = Medicine
    template_name = 'client/start_page.html'
    context_object_name = 'medicines'



def register_client(request):
    if request.method == 'POST':
        user_form = CustomUserRegistrationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST)
        
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()

            cart = Cart()
            cart.user = client
            cart.save()
            
            login(request, user)
            return redirect('start_page')
    else:
        user_form = CustomUserRegistrationForm()
        client_form = ClientRegistrationForm()



    return render(request, 'client/registration.html', {'user_form': user_form, 'client_form': client_form})


@login_required
def add_to_favorites(request, slug):
    medicine = Medicine.objects.get(slug = slug)
    client = get_object_or_404(Client, user=request.user)
    if not Favourite.objects.filter(client=client, medicine=medicine).exists():
        Favourite.objects.create(client=client, medicine=medicine)

    return redirect('medicine_detail', slug=slug)


@login_required
def remove_from_favorites(request, slug):
    medicine = Medicine.objects.get(slug = slug)
    client = request.user.client

    favorite_medicine = Favourite.objects.filter(client=client, medicine=medicine)
    if favorite_medicine.exists():
        favorite_medicine.delete()

    return redirect('medicine_detail', slug=slug)


def logout_client(request):
    logout(request)
    return redirect('login')


class LoginPageView(LoginView):
    template_name = 'client/login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('start_page')


class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'client/medicine_detail.html'
    slug_param = 'slug'
    slug_url_kwarg = 'slug'    



class UserProfileView(TemplateView):
    template_name = 'client/profile.html'




@login_required
def cart_view(request):
    client = get_object_or_404(Client, user=request.user)
    cart =  get_object_or_404(Cart, user=client)
    
    if request.method == 'POST':
        form = ClientOrderForm(request.POST)
        if form.is_valid():
            pharmacy = form.cleaned_data['pharmacy']
            print(pharmacy)
        order = Order.objects.create(user=client, total_price=cart.total_price, pharmacy=pharmacy)
        cart_items = cart.cartitems.all()


        for cart_item in cart_items:
            order.order_items.create(medicine=cart_item.medicine, quantity=cart_item.quantity)
    
        cart.cartitems.all().delete()
        cart.total_price = 0
        cart.save()
        
        return redirect('order_list')

    else:
        form = ClientOrderForm()
        cart_items = CartItem.objects.filter(cart=cart)

 


    context = {
                'cart': cart_items,
                'form':form,
                'total_price':cart.total_price
                }
    return render(request, 'client/cart.html', context)
    

@login_required
def add_medicine_to_cart(request, slug):
    client = get_object_or_404(Client, user=request.user)
    medicine = get_object_or_404(Medicine, slug=slug)
    cart = get_object_or_404(Cart, user=client)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        medicine=medicine
    )

    current_url = resolve(request.path_info).url_name
    return redirect('start_page')



def orders_list(request):
    client = get_object_or_404(Client, user=request.user)
    orders = Order.objects.filter(user=client)
    

    context = {'orders': orders}
    return render(request, 'client/order_list.html', context)


def order_details(request, link):
    order_items = OrderItem.objects.filter(order=link)


    context ={
        'orders':order_items
        }
    
    return render(request, 'client/order_details.html', context)



class FavoritesPage(ListView):
    model = Favourite
    template_name = 'client/favorites.html'
    context_object_name = 'favorites'

    


