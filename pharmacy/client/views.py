from django.shortcuts import get_object_or_404, render, get_list_or_404
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from .models import Medicine
from django.views.generic import CreateView, ListView, DetailView, DeleteView, TemplateView, UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import resolve, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from geopy.geocoders import Nominatim
import folium
from haversine import haversine
from geopy.distance import geodesic

def show_map(request):
    pharmacies = Pharmacy.objects.all()
    if request.method == 'POST':
        location = request.POST.get('location', '')
        
        # Используем Geopy, чтобы получить координаты по введенному местоположению
        geolocator = Nominatim(user_agent="your_app_name")
        location_data = geolocator.geocode(location)



    # Если запрос GET, просто отображаем пустую карту
    my_map = folium.Map(location=[0, 0], zoom_start=2)
    context = {'map': my_map._repr_html_(), 'location': ''}
    return render(request, 'map_template.html', context)




class TheStartPage(ListView):
    model = Medicine
    template_name = 'client/start_page.html'
    context_object_name = 'medicines'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Поиск по названию товара
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        # Фильтр по цене
        price_filter = self.request.GET.get('price', '')
        if price_filter:
            queryset = queryset.filter(price=price_filter)
        
        # Фильтр по цене (больше чем)
        price_greater_than = self.request.GET.get('price_greater_than', '')
        if price_greater_than:
            queryset = queryset.filter(price__gt=price_greater_than)
        
        # Фильтр по цене (меньше чем)
        price_less_than = self.request.GET.get('price_less_than', '')
        if price_less_than:
            queryset = queryset.filter(price__lt=price_less_than)
        
        # Фильтр по дате производства
        manufacturing_date = self.request.GET.get('manufacturing_date', '')
        if manufacturing_date:
            queryset = queryset.filter(manuf_date=manufacturing_date)
        
        return queryset

def update_profile_view(request, link):
    # Retrieve the object to be updated
    client = get_object_or_404(Client, id=link)

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST, instance=client)
        form2 = CUUF(request.POST, instance=client)  # Pass the instance to CUUF form
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('profile')  # Redirect to the success URL
    else:
        form = ClientRegistrationForm(instance=client)
        form2 = CUUF(instance=client)  # Pass the instance to CUUF form

    return render(request, 'client/update-client.html', {'form': form, 'form2': form2})


def register_client(request):
    if request.method == 'POST':
        user_form = CustomUserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            client = Client.objects.create(user=user)
        
            cart = Cart()
            cart.user = client
            cart.save()
            
            login(request, user)
            return redirect('start_page')
    else:
        user_form = CustomUserRegistrationForm()




    return render(request, 'client/registration.html', {'user_form': user_form})


@login_required
def change_quantity(request, slug, param):
    medicine = get_object_or_404(Medicine, slug=slug)
    cart_items = get_list_or_404(CartItem, medicine=medicine)

    for cart_item in cart_items:
        if param == 'incr':
            cart_item.increase_quantity()
        elif param == 'decr':
            cart_item.decrease_quantity()
    return redirect('cart')


@login_required
def remove_product_from_cart(request, slug):
    medicine = get_object_or_404(Medicine, slug=slug)
    cart_item = get_object_or_404(CartItem, medicine=medicine)

    cart_item.delete()

    return redirect('cart')




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

    return redirect('favorites')



def logout_client(request):
    logout(request)
    return redirect('login')


class LoginPageView(LoginView):
    template_name = 'client/login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('start_page')


def medicine_detail_view(request, slug):
    try:
        client = get_object_or_404(Client, user=request.user)
    except:
        print('boom')
    comments = Comment.objects.all()
    flag1 = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.client = client
            new_comment.save()
            form = CommentForm()  # Reset the form after saving a comment
    else:
        form = CommentForm()
    if 'delete_comment' in request.POST:
        comment_id = request.POST['delete_comment']
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return redirect('medicine_detail', slug=slug)

    client = get_object_or_404(Client, user=request.user)
    medicine = get_object_or_404(Medicine, slug=slug)
    favorites = Favourite.objects.filter(client=client)
    flag = None
    for fav in favorites:
        if slug == fav.medicine.slug:  
            print(flag)
            flag = True
            break
        else:
            flag = False

    context = {'medicine': medicine,
               'flag':flag,
               'comments': comments, 
               'form': form,}
    return render(request, 'client/medicine_detail.html', context) 



class UserProfileView(TemplateView):
    template_name = 'client/profile.html'




@login_required
def cart_view(request):
    client = get_object_or_404(Client, user=request.user)
    cart = get_object_or_404(Cart, user=client)
    pharmacies = Pharmacy.objects.all()
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    f = lat
    s = lon
    print(f, s)
    best_pharmacy = None
    best_distance = float('inf')
    
    try:
        if f is not None and s is not None:
            point2 = (float(f), float(s))
            
        
        geolocator = Nominatim(user_agent="client")
        location = geolocator.reverse((f, s), language="ru")

        for pharm in pharmacies:
            point1 = (pharm.latitude, pharm.longitude)
            distance_km = geodesic(point2, point1).kilometers
            print(distance_km, 'км')
            if distance_km < best_distance:
                    best_distance = distance_km
                    best_pharmacy = pharm

            if best_pharmacy is not None:
                print(best_pharmacy.id)
                print(best_pharmacy.address)
                client.temp_pharmacy = best_pharmacy
                client.best_distance = best_distance
                client.save()
                print("Best Pharmacy:", best_pharmacy)
            
                

    except:
        print("Error:")
   
        

    if request.method == 'POST':
        order_form = ClientOrderForm(request.POST)
        if order_form.is_valid():
            order = Order.objects.create(
                user=client,
                total_price=cart.total_price,
                pharmacy=client.temp_pharmacy
            )

            cart_items = cart.cartitems.all()

            for cart_item in cart_items:
                order.order_items.create(
                    medicine=cart_item.medicine,
                    quantity=cart_item.quantity
                )

            cart.cartitems.all().delete()
            cart.total_price = 0
            cart.save()

            return redirect('order_list')
    else:
        order_form = ClientOrderForm()

    cart_items = CartItem.objects.filter(cart=cart)

    context = {
                    'cart': cart_items,
                    'total_price':cart.total_price,
                    'pharmacies': pharmacies,
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



def favorites_page(request):
    client = get_object_or_404(Client, user=request.user)
    favs = Favourite.objects.filter(client=client)

    context = {
        'favorites':favs
    }
    return render(request, 'client/favorites.html', context)
    


