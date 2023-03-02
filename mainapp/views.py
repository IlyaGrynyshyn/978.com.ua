from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Min, Max, Count, Q
from cart.cart import Cart
from specs.models import ProductFeatures, CategoryFeature
from .recently_viewed import RecentlyViewed

from mainapp.models import Product, Category, TopCategory, Banner, ProductImage


class BaseListView(ListView):
    model = Product
    template_name = "mainapp/mainpage.html"
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        res = RecentlyViewed(self.request)
        product_slug = res.recently_viewed.keys()
        products = Product.objects.filter(slug__in=product_slug)
        context['recently_viewed'] = products.reverse()
        context['top_category'] = TopCategory.objects.all()
        context['banner'] = Banner.objects.all().order_by('-id')
        context['top_products'] = Product.objects.filter(section__title='Top Deal')
        context['cart'] = Cart(self.request)
        context['categories'] = Category.objects.filter(top_category=None)
        context['popular_products'] = Product.objects.all().order_by('-popular')[0:12]
        return context


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class CategoryListView(DetailView):
    model = Category
    filterset_class = FilteredListView
    template_name = 'mainapp/product_list.html'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(category=self.get_object()).select_related('category')
        context = super(CategoryListView, self).get_context_data(object_list=object_list, **kwargs)
        res = RecentlyViewed(self.request)
        product_slug = res.recently_viewed.keys()
        products = Product.objects.filter(slug__in=product_slug)
        context['recently_viewed'] = products.reverse()
        context['cart'] = Cart(self.request)
        context['categories'] = Category.objects.all().select_related('top_category')
        context['category_slug'] = self.kwargs.get('category_slug')
        context['top_category_slug'] = self.kwargs.get('top_category_slug')
        context['top_category'] = TopCategory.objects.all()
        query = self.request.GET.get('q')
        category = self.get_object()
        context['category'] = category
        context['product_count'] = Product.objects.filter(category=self.get_object()).aggregate(Count('id'))
        order = self.request.GET.get('orderby')
        minMaxPrice = Product.objects.category_product(category=category).aggregate(Min('price'), Max('price'))
        context['minMaxPrice'] = minMaxPrice
        context['order'] = order
        price_max = self.request.GET.get('price_max')
        price_min = self.request.GET.get('price_min')
        # if not query and not self.request.GET:
        #     products = Product.objects.category_product(category=category)

        # products = Product.objects.search(query=query)
        url_kwargs = {}
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)
        q_condition_queries = Q()
        for key, value in url_kwargs.items():
            if isinstance(value, list):
                q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
            else:
                q_condition_queries.add(Q(**{'value': value}), Q.OR)
        pf = ProductFeatures.objects.filter(
            q_condition_queries
        ).prefetch_related('product', 'feature').values('product_id')
        product_filter = Product.objects.filter(category=category).filter(
            id__in=[pf_['product_id'] for pf_ in pf]).prefetch_related('features')
        context['product_filter'] = product_filter
        # products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf]).prefetch_related('features')
        products = Product.objects.category_product(category=category)
        # products = Product.objects.category_product(category=category).filter(
        #     id__in=[pf_['product_id'] for pf_ in pf]).prefetch_related('features')
        if order:
            products = Product.objects.order(category=category, order_by=order)
        if query:
            products = category.product_set.filter(Q(title__icontains=query))
        if price_min:
            products = Product.objects.filter(price__gte=price_min).filter(price__lte=price_max)
        paginator = Paginator(products, 24)  # paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        context['page_obj'] = activities
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'mainapp/product_page_V2.html'
    slug_url_kwarg = 'product_slug'
    extra_context = {'title': "Каталог продуктів"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product1 = self.get_object()
        res = RecentlyViewed(self.request)
        res.viewed(product1)
        product_slug = res.recently_viewed.keys()
        products = Product.objects.filter(slug__in=product_slug)
        context['recently_viewed'] = products
        context['cart'] = Cart(self.request)
        context['top_category'] = TopCategory.objects.all()
        context['image'] = ProductImage.objects.filter().select_related('product')
        context['categories'] = Category.objects.filter(top_category=None)
        context['top_products'] = Product.objects.filter(section__title='Top Deal')
        product1.popular = product1.popular + 1
        product1.save()
        return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def search(request):
    if is_ajax(request=request):
        product = request.POST.get('product')
        res = None
        qs = Product.objects.filter(title__icontains=product).select_related('section', 'tag', 'category')
        product_image = ProductImage.objects.all().select_related('product')
        if len(qs) > 0 and len(product) > 0:
            data = []
            for pos in qs:
                item = {
                    'url': pos.get_absolute_url(),
                    'title': pos.title,
                    'price': pos.price,
                    'img': product_image.filter(product__slug=pos.slug).first().img.url
                }
                data.append(item)
            res = data
        else:
            res = 'За вашим запитом нічого не знайдено...'
        return JsonResponse({'data': res})
    return JsonResponse({})


def search_page(request):
    category_slug = request.GET.get('category_slug')
    top_category_slug = request.GET.get('top_category_slug')
    q = request.GET.get('q')
    data = Product.objects.search(query=q)
    context = {
        'products': data,
        'top_category': TopCategory.objects.all(),
        'cart': Cart(request),
        'category_slug': category_slug,
        'top_category_slug': top_category_slug
    }
    return render(request, 'mainapp/search_result.html', context)


def test(request):
    return render(request, 'mainapp/test.html')
