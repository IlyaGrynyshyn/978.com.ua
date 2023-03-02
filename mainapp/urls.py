from django.urls import path
from .views import BaseListView, ProductDetailView, CategoryListView, search, search_page, test

urlpatterns = [
    path('', BaseListView.as_view(), name='home'),
    path('product/<slug:product_slug>', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:top_category_slug>/<slug:category_slug>', CategoryListView.as_view(), name='category_detail'),
    path('search/', search, name='search'),
    path('search_page/', search_page, name='search_page'),
    path('test/', test)

]
