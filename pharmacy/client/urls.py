from django.urls import path
from .views import *

urlpatterns = [
    path('', TheStartPage.as_view(), name='start_page'),
    path('profile/', UserProfileView.as_view(), name='profile'),


    path('cart/add/<slug:slug>/', add_medicine_to_cart, name='cart_add'),
    path('cart/', cart_view, name='cart'),


    # medicine
    path('medicine-detail/<slug:slug>/', MedicineDetailView.as_view(), name='medicine_detail'),


    # auth
    path('registration/', register_client, name='registration'),
    path('logout/', logout_client, name='logout'),
    path('login/', LoginPageView.as_view(), name='login')
]