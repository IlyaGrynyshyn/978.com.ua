from django.urls import path
from .views import order_create,success_order

app_name = 'order'

urlpatterns = [
    path('checout/', order_create, name='order_create'),
    path('success-order/', success_order, name='success_order')
]
