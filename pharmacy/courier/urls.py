from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TheStartPage, name='start_page_c'),

    # login
    path('registration/', register_courier, name='registration_c'),
    path('logout/', logout_courier, name='logout_c'),
    path('login/', LoginPageView.as_view(), name='login_c'),

    # profile
    path('profile/', UserProfileView.as_view(), name='profile_c'),
    
    # orders
    path('order/<str:link>/', order_details, name='order_details_c'),
    path('order/<str:link>/decline_delivery', decline_delivery,name='decline_delivery')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)