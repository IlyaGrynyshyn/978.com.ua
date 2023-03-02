from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import *


class PhotoAdmin(admin.StackedInline):
    model = ProductImage





# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'image_show', 'category', 'product_code', 'qty_product', 'price', 'section', 'tag')
#     list_display_links = ('id', 'title')
#     list_editable = ('section', 'tag',)
#     search_fields = ('title', 'product_code')
#     prepopulated_fields = {"slug": ("title",)}
#     inlines = [PhotoAdmin, Additional_Information]
#
#     def image_show(self, obj):
#         if obj.img:
#             return mark_safe(f"<img src='{obj.img.url}' width='60' /> ")
#         return None
#
#     image_show.__name__ = 'Фотокартка'
class ProdcutResource(resources.ModelResource):

    class Meta:
        model = Product


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProdcutResource
    list_display = ('id', 'title', 'category', 'product_code', 'qty_product', 'price', 'section', 'tag')
    list_display_links = ('id', 'title')
    list_editable = ('section', 'tag',)
    search_fields = ('title', 'product_code')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PhotoAdmin,]


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}


class TopCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'top_category')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(TopCategory, TopCategoryAdmin)
admin.site.register(Banner)
admin.site.register(Section)
admin.site.register(Tag)
