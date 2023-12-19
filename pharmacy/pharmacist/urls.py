from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TheStartPage.as_view(), name='start_page_pharmacist'),
    path('profile/', UserProfileView.as_view(), name='profile_pharmacist'),

    # orders
    path('orders/', orders_handling, name='orders_handling'),
    path('orders/<str:link>/', order_details, name='order_details_ph'),
    path('order/<str:link>/decline', decline_order, name='decline_order'),


    path('add_medicine/', CreateMedicineView.as_view(), name='add_medicine'),
    path('ph_meds/', ph_meds, name='ph_meds'),
    path('medicine-detail/<slug:slug>/', MedicineDetailView.as_view(), name='medicine_detail_pharmacist'),
    path('medicine-detail/<slug:slug>/update/', MedicineUpdateView.as_view(), name='update_med'),


    # auth
    path('registration/', register_pharmacist, name='registration_pharmacist'),
    path('logout/', logout_pharmacist, name='logout_pharmacist'),
    path('login/', LoginPageView.as_view(), name='login_pharmacist')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)