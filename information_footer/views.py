from django.shortcuts import render


def delivery_and_payment(request):
    return render(request, 'information_footer/delivery_and_payment.html')


def warranty(request):
    return render(request, 'information_footer/warranty.html')


def return_add_exchange(request):
    return render(request, 'information_footer/return-and-exchang.html')


def contact(request):
    return render(request, 'information_footer/contacts.html')


def partner(request):
    return render(request, 'information_footer/partner.html')


def about_us(request):
    return render(request, 'information_footer/about_us.html')
