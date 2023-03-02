
from django.contrib import admin


from delivery.models import DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):

    list_display = ['name', 'code']
