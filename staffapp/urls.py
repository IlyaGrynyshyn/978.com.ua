from django.urls import path

from staffapp.views import ordered_product,OrderList

urlpatterns = [
    path('ordered_product/', OrderList.as_view(), name='Order_list')
]
