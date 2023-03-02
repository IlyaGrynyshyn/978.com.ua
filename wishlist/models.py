from django.conf import settings
from django.db import models
from mainapp.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)  # here CASCADE is the behavior to adopt when the referenced object(because it is a foreign key) is deleted. it is not specific to django,this is an sql standard.
    wished_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.wished_item.title
