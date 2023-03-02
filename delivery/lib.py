from model_search import model_search
import requests

from delivery.models import Warehouse, City, DeliveryMethod
from gip_west import settings


def search_warehouses(delivery_method_id, city, query, limit=None):
    if not query or not city or not delivery_method_id:
        return []

    try:
        city = city
    except Exception:
        return []

    try:
        delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
    except DeliveryMethod.DoesNotExist:
        return []

    warehouses = Warehouse.objects.filter(
        delivery_method__code=delivery_method.code,
        city__name=city
    )

    queryset = model_search(query, warehouses, ['name'])

    if limit is not None:
        return queryset[:limit]

    return queryset


def search_cities(query, limit=None):
    if not query:
        return []

    queryset = model_search(query, City.objects.all(), ['name'])

    if limit is not None:
        return queryset[:limit]

    return queryset


def refresh_cities():
    api_domain = 'https://api.novaposhta.ua'

    api_path = '/v2.0/json/Address/getCities'

    api_data = {
        "modelName": "Address",
        "calledMethod": "getCities",
        'apiKey': settings.NOVA_POSHTA_API_KEY
    }

    response = requests.post(api_domain + api_path, json=api_data).json()
    print(response)

    if not response.get('success'):
        raise Exception(','.join(response.get('errors')))

    City.objects.all().delete()

    cities = []

    for item in response.get('data'):
        params = {
            'name': item.get('Description'),
            'reference': item.get('Ref')
        }

        cities.append(City(**params))

    City.objects.bulk_create(cities)


def refresh_warehouses():
    global params
    api_domain = 'https://api.novaposhta.ua'

    api_path = '/v2.0/json/Address/getWarehouses'

    api_data = {
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        'apiKey': settings.NOVA_POSHTA_API_KEY
    }

    response = requests.post(api_domain + api_path, json=api_data).json()

    if not response.get('success'):
        raise Exception(','.join(response.get('errors')))

    Warehouse.objects.all().delete()

    warehouses = []

    for item in response.get('data'):
        try:
            params = {
                'name': item.get('Description'),
                'reference': item.get('Ref'),
                # 'city_id': City.objects.get('id').filter(name=item.get("CityDescription")),
                'city': City.objects.get(reference=item.get("CityRef")),
                'delivery_method_id': 1
            }
            warehouses.append(Warehouse(**params))
        except:
            print(item.get('CityRef'))
    Warehouse.objects.bulk_create(warehouses)
