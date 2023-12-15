from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TheStartPage.as_view(), name='start_page'),
    path('profile/', UserProfileView.as_view(), name='profile'),


    path('cart/add/<slug:slug>/', add_medicine_to_cart, name='cart_add'),
    path('cart/', cart_view, name='cart'),


    # medicine
    path('medicine-detail/<slug:slug>/', MedicineDetailView.as_view(), name='medicine_detail'),
    path('profile/my-orders/', orders_list, name='order_list'),
    path('profile/my-orders/<str:link>/details/', order_details, name='order_details'),

    path('add_to_favorites/<slug:slug>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<slug:slug>/', remove_from_favorites, name='remove_from_favorites'),
    path('profile/favorites/', FavoritesPage.as_view(), name='favorites'),

    # auth
    path('registration/', register_client, name='registration'),
    path('logout/', logout_client, name='logout'),
    path('login/', LoginPageView.as_view(), name='login')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)