from django.urls import path
from .views import wishlist, add_to_wishlist, remove_from_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist, name='wishlist'),
    path('add/<slug:product_slug>', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<slug:product_slug>', remove_from_wishlist, name='remove_wishlist')
]
