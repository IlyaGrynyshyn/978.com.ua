from decimal import Decimal

from gip_west import settings
from mainapp.models import Product


class RecentlyViewed:
    def __init__(self, request):
        self.session = request.session
        recently_viewed = self.session.get(settings.RECENTLY_VIEWED)
        if not recently_viewed:
            # save an empty cart in the session
            recently_viewed = self.session[settings.RECENTLY_VIEWED] = {}
        self.recently_viewed = recently_viewed


    def viewed(self, product):
        product_id = str(product.slug)
        print(str(product_id))
        if self.recently_viewed:
            if product_id in self.recently_viewed:
                del self.recently_viewed[product_id]
            self.recently_viewed[product_id] = {'product_title': product.title, 'product_price': product.price}
            if len(self.recently_viewed) > 12:
                self.recently_viewed.popitem()
        else:
            self.recently_viewed[product_id] = {'product_title': product.title, 'product_price': product.price}
        self.session.modified = True

    def __iter__(self):
        product_slug = self.recently_viewed.keys()
        products = Product.objects.filter(slug__in=product_slug)
        res = self.recently_viewed.copy()
        for product in products:
            res[str(product.slug)]['product'] = product
            return


    def save(self):
        """
        mark the session as "modified" to make sure it gets saved
        """
        self.session.modified = True

    def clear(self):
        """
        remove all from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
