from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from delivery.lib import search_warehouses, search_cities, refresh_cities, refresh_warehouses


def get_warehouses(request):
    warehouses = search_warehouses(
        request.GET.get('delivery_method'),
        request.GET.get('city'),
        request.GET.get('query'),
        limit=10)

    suggestions = [w.name for w in warehouses]

    return JsonResponse({
        'query': request.GET.get('query'),
        'suggestions': suggestions
    })


def get_cities(request):
    query = request.GET.get('query')
    print(query)

    suggestions = [str(c) for c in search_cities(query, limit=50)]
    print(suggestions)

    return JsonResponse({
        'query': query,
        'suggestions': suggestions
    })


def see(request):
    from .forms import DeliveryForm
    return render(request, 'delivery/form.html', {'form': DeliveryForm})


def refresh(request):
    refresh_cities()
    refresh_warehouses()
    return HttpResponse('Warehouses were successfully refreshed')
