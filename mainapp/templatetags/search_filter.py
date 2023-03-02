# from collections import defaultdict
#
# from django import template
# from django.utils.safestring import mark_safe
#
# from specs.models import ProductFeatures
#
# register = template.Library()
#
#
# @register.filter
# def product_spec(category):
#     product_features = ProductFeatures.objects.filter(product__category=category).select_related('product', 'feature')
#     feature_and_values = defaultdict(list)
#     for product_feature in product_features:
#         if product_feature.value not in feature_and_values[
#             (product_feature.feature.feature_name, product_feature.feature.feature_filter_name)]:
#             feature_and_values[
#                 (product_feature.feature.feature_name, product_feature.feature.feature_filter_name)
#             ].append(product_feature.value)
#     search_filter_body = """<div class="ocf-filter"><div class="catalog-filter__group catalog-filter__select active">{}</div></div>"""
#     collect_feature_value = """<div class="ocf-value-list"><div class='catalog-filter__group-content  catalog-filter__select-box'>{}</div></div>"""
#     mid_res = ""
#     for (feature_name, feature_filter_name), feature_values in feature_and_values.items():
#         feature_name_html = f"""<h3 class="catalog-filter__group-title"><span class="ocf-filter-name">{feature_name}</span></h3>"""
#         feature_values_res = ""
#         for f_v in feature_values:
#             mid_feature_values_res = \
#                 "<div class='catalog_filter_group'><label class='catalog_filter_group_item'>{feature_name}<input type='checkbox' name='{f_f_name}' " \
#                 "value='{feature_name}'><span class='checkmark'></span></label></div>".format(
#                     feature_name=f_v, f_f_name=feature_filter_name
#                 )
#             feature_values_res += mid_feature_values_res
#         col = collect_feature_value.format(feature_values_res)
#         feature_name_html += col
#         mid_res += feature_name_html + ''
#     res = search_filter_body.format(mid_res)
#     return mark_safe(res)

from collections import defaultdict

from django import template
from django.utils.safestring import mark_safe

from specs.models import ProductFeatures

register = template.Library()


@register.filter
def product_spec(category):
    product_features = ProductFeatures.objects.filter(product__category=category).select_related('product', 'feature')
    feature_and_values = defaultdict(list)
    for product_feature in product_features:
        if product_feature.value not in feature_and_values[
            (product_feature.feature.feature_name, product_feature.feature.feature_filter_name)]:
            feature_and_values[
                (product_feature.feature.feature_name, product_feature.feature.feature_filter_name)
            ].append(product_feature.value)
    search_filter_body = """<div class="ocf-filter"><div class="catalog-filter__group catalog-filter__select active">{}</div></div>"""
    collect_feature_value = """<div class="ocf-value-list"><div class='catalog-filter__group-content  catalog-filter__select-box'>{}</div></div>"""
    mid_res = ""
    for (feature_name, feature_filter_name), feature_values in feature_and_values.items():
        feature_name_html = f"""<div class="catalog-filter__group-title"><span class="ocf-filter-name">{feature_name}</span></div>"""
        feature_values_res = ""
        for f_v in feature_values:
            mid_feature_values_res = \
                "<div class='catalog_filter_group'><label class='catalog_filter_group_item'>{feature_name}<input type='checkbox' name='{f_f_name}' " \
                "value='{feature_name}'><span class='checkmark'></span></label></div>".format(
                    feature_name=f_v, f_f_name=feature_filter_name
                )
            feature_values_res += mid_feature_values_res
        col = collect_feature_value.format(feature_values_res)
        feature_name_html += col
        mid_res += feature_name_html + ''
    res = search_filter_body.format(mid_res)
    return mark_safe(res)
