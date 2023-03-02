from django.shortcuts import render

from cart.cart import Cart
from mainapp.models import TopCategory, Category
from .models import OrderItem, Order
from .forms import OrderCreateForm
from delivery.forms import DeliveryForm
from mainapp.models import Product
from delivery.models import DeliveryMethod, City, Warehouse


def order_create(request):
    cart = Cart(request)
    categories = TopCategory.objects.all()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.delivery_method = form.fields['delivery'].get_delivery_method()
            order.city = City.objects.get(name=form.fields['delivery'].get_city())
            order.warehouse = Warehouse.objects.get(name=form.fields['delivery'].get_warehouse())
            if request.user.is_authenticated:
                order.customer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
                # product = Product.objects.filter(title__icontains=item['product']).update(ordered=+int(1))

            cart.clear()
            return render(request, 'order/created.html', {'cart': cart, 'order': order, 'top_category': categories})
    else:
        form = OrderCreateForm()
    return render(request, 'order/checkout.html', {'cart': cart, 'form': form, 'top_category': categories})


def success_order(request):
    cart = Cart(request)
    categories = Category.objects.all()
    context = {
        'top_category': TopCategory.objects.all(),
        'cart': cart
    }
    return render(request, 'order/success_order.html', context)
