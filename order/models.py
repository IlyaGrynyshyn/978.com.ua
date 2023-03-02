from django.db import models

from gip_west import settings
from mainapp.models import Product

STATUS_NEW = 'new'
STATUS_IN_PROGRESS = 'in_progress'
STATUS_READY = 'is_ready'
STATUS_COMPLETED = 'completed'

BUYING_TYPE_SELF = 'self'
BUYING_TYPE_DELIVERY = 'delivery'

DELIVERY_TYPE_NOVA_POST = 'NOVA POST'
DELIVERY_TYPE_NOVA_DELIVERY = 'NOVA DELIVERY'

STATUS_CHOICES = (
    (STATUS_NEW, 'Нове замовлення'),
    (STATUS_IN_PROGRESS, 'Замовлення в обробці'),
    (STATUS_READY, 'Замовлення готове'),
    (STATUS_COMPLETED, 'Замовлення виконано')
)
DELIVERY_TYPE = (
    (DELIVERY_TYPE_NOVA_POST, "У відділення Нова пошта"),
    (DELIVERY_TYPE_NOVA_DELIVERY, "Доставка кур'єром Нова пошта")
)


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Користувач')
    first_name = models.CharField(max_length=50, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')
    midl_name = models.CharField(max_length=50, verbose_name='По батькові')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(verbose_name='Номер телефону', max_length=15)

    from delivery.models import DeliveryMethodField, CityField, WarehouseField

    delivery_method = DeliveryMethodField()
    city = CityField()
    warehouse = WarehouseField()

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')
    updated = models.DateTimeField(auto_now=True, verbose_name='Зміни в замовлені')
    paid = models.BooleanField(default=False, verbose_name='Сплачено')
    comment = models.TextField(verbose_name='Коментар до замовлення', null=True, blank=True)
    call_back = models.BooleanField(default=False, verbose_name='Чи передзвонити?')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def count_items(self):
        return self.items.count()

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ('-created',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    # total_price = models.DecimalField(max_digits=10)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

