import http
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mainapp.models import Product, Category
from .cart import Cart


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def add_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add_quantity(product)
    return redirect(request.META['HTTP_REFERER'])


def subtraction_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.subtraction_quantity(product)
    return redirect(request.META['HTTP_REFERER'])


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})
