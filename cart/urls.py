from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('add_qty/<int:product_id>/', add_quantity, name='change_qty'),
    path('subtraction_quantity/<int:product_id>/', subtraction_quantity, name='subtraction_quantity')
]
