from django.shortcuts import render, redirect
from mainapp.models import Product
from wishlist.models import Wishlist
from django.contrib.auth.decorators import login_required


@login_required
def add_to_wishlist(request, product_slug):
    # Отримуємо продукт, який був доданий до списку бажань
    product = Product.objects.get(slug=product_slug)

    # Перевіряємо, чи вже додано до списку бажань
    if Wishlist.objects.filter(wished_item=product, user=request.user).exists():
        return redirect('product_detail', product_slug=product_slug)
    # Створюємо новий запис списку бажань
    wishlist = Wishlist(wished_item=product, user=request.user)
    wishlist.save()

    return redirect('wishlist:wishlist')


@login_required
def wishlist(request):
    # Отримуємо всі записи списку бажань для даного користувача
    wishlist_items = Wishlist.objects.filter(user=request.user)

    context = {'wishlist_items': wishlist_items}

    return render(request, 'wishlist/wishlist_base.html', context)


@login_required
def remove_from_wishlist(request, product_slug):
    # Отримуємо запис списку бажань для видалення
    wishlist_item = Wishlist.objects.get(slug=product_slug)

    # Видаляємо запис списку бажань
    wishlist_item.delete()

    return redirect('wishlist')
