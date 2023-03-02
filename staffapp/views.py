from django.db.models import QuerySet
from django.shortcuts import render
from order.models import OrderItem, Order
from django.views.generic import ListView


def ordered_product(request):
    context = {
        'ordered_product': OrderItem.objects.all()
    }
    return render(request, 'staffapp/ordered-product.html', context=context)


class OrderList(ListView):
    model = Order
    template_name = 'staffapp/ordered-product.html'
    context_object_name = 'ordered_product'
    paginate_by = 100

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        query = OrderItem.objects.all().query
        query.group_by = ['order_id']
        context['order_item'] = QuerySet(query=query, model=OrderItem)
        return context

