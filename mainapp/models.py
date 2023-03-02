import random

from django.db import models
from django.db.models import Q
from django.urls import reverse

from gip_west import settings
from ckeditor.fields import RichTextField


def content_file_name(instance, filename):
    return f"images/{instance.__class__.__name__}/{instance.title}/{filename}"


class TopCategory(models.Model):
    """
    Модель яка відповідає за загальну назву категорії.
    Наприклад: Телефони.
    """
    title = models.CharField(max_length=50, verbose_name="Ім'я найвищої категорії")
    slug = models.SlugField(unique=True, db_index=True)
    category_icon = models.ImageField(upload_to=content_file_name, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("top_category_detail", kwargs={'top_category_slug': self.slug})

    class Meta:
        verbose_name = 'Найвища категорія'
        verbose_name_plural = 'Найвищі категорії'


class Category(models.Model):
    """
    Модель яка відповідає за підкатегорію.
    Наприклад: Смартфон Apple.
    """
    top_category = models.ForeignKey(TopCategory, verbose_name='Головна категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name="Ім'я категорії")
    slug = models.SlugField(unique=True, db_index=True)
    vendor_code = models.BigIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'top_category_slug': self.top_category.slug, 'category_slug': self.slug}
        return reverse("category_detail", kwargs=kwargs)

    class Meta:
        verbose_name = 'Категорії'
        verbose_name_plural = 'Категорії'


def get_product_code():  # На період розробки, щоб не запарюватись з вводом коду продукти.
    if settings.DEBUG:
        code = random.randint(100000, 999999)
        return code
    return None


class ProductQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        return Product.objects.filter(Q(title__icontains=query))

    def category_product(self,category):
        return Product.objects.filter(category=category)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def order(self, category, order_by):
        return Product.objects.filter(category=category).order_by(f'{order_by}')

    def category_product(self, category):
        return self.get_queryset().category_product(category=category)

class Product(models.Model):
    """
    Модель відповідає за продукт.
    """
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Назва')
    slug = models.SlugField(unique=True, db_index=True, max_length=255)
    product_code = models.IntegerField(verbose_name='Код продукту')
    price = models.IntegerField(verbose_name='Ціна')
    new_price = models.IntegerField(null=True, blank=True, verbose_name='Нова ціна')
    description = RichTextField(verbose_name='Опис', null=True, blank=True)
    section = models.ForeignKey("Section", on_delete=models.DO_NOTHING, null=True, blank=True)
    tag = models.ForeignKey('Tag', on_delete=models.DO_NOTHING, null=True, blank=True)
    qty_product = models.IntegerField(default=1, verbose_name='Кількість товару', null=True, blank=True)
    ordered = models.IntegerField(default=0, verbose_name='Замовлено разів')
    popular = models.IntegerField(default=1, verbose_name='Разів переглянуто')
    features = models.ManyToManyField("specs.ProductFeatures", blank=True, related_name='features_for_product')
    supplier_product_url = models.URLField(verbose_name='Посилання на товар', null=True, blank=True)
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_features(self):
        return {f.feature.feature_name: ' '.join([f.value, f.feature.unit or ""]) for f in self.features.all().select_related('feature')}

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Продукція'
        verbose_name_plural = 'Продукція'
        ordering = ['-id']


class ProductImage(models.Model):
    """
    Модель відповідає за фото до продукту
    """

    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=f'images/product/')

    def __str__(self):
        return self.product.title

    class Meta:
        ordering = ['-id']


class Section(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    title = models.CharField(max_length=22)
    color = models.CharField(max_length=50, default="#eda526")
    background = models.CharField(max_length=50, default='#eda526')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Тег'
        ordering = ['-id']


class Banner(models.Model):
    image = models.ImageField(upload_to=content_file_name)
    slug = models.SlugField()
    title = models.CharField(max_length=155)
    subtitle = models.CharField(max_length=155)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'banner_slug': self.slug})

    class Meta:
        verbose_name = 'Банер'
        verbose_name_plural = 'Банер'
        ordering = ['-id']


