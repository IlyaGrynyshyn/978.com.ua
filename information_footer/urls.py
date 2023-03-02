from django.urls import path
from .views import delivery_and_payment, warranty, return_add_exchange, contact, partner, about_us

app_name = 'footer'

urlpatterns = [
    path('delivery_and_payment/', delivery_and_payment, name='delivery_and_payment'),
    path('warranty/', warranty, name='warranty'),
    path('return-and-exchange/', return_add_exchange, name='return-and-exchange'),
    path('contact/', contact, name='contact'),
    path('partner/', partner, name='partner'),
    path('about_us/', about_us, name='about_us')
]
