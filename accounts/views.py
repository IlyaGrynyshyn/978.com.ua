from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from cart.cart import Cart
from mainapp.models import TopCategory
from order.models import Order, OrderItem
from .forms import LoginForm, RegistrationForm, PasswordChangingForm, PasswordsResetForm
from django.views.generic import ListView


class LoginDetailView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        top_category = TopCategory.objects.all()
        context = {
            'form': form,
            'top_category': top_category,
            'cart': Cart(request)
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
            'top_category': TopCategory.objects.all(),
            'cart': Cart(request)
        }
        return render(request, 'accounts/login.html', context)


class RegistrationView(CreateView):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        top_category = TopCategory.objects.all()
        context = {
            'form': form,
            'top_category': top_category,
            'cart': Cart(request)
        }
        return render(request, 'accounts/registration.html', context=context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.email = form.cleaned_data['email']
            new_user.phone = form.cleaned_data['phone']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(
                username=new_user.email or new_user.phone, password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('accounts:account_detail')
        top_category = TopCategory.objects.all()
        context = {
            'form': form,
            'top_category': top_category
        }
        return render(request, 'accounts/registration.html', context)


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('accounts:account_detail')

    @method_decorator(login_required(login_url="accounts:login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['top_category'] = TopCategory.objects.all()
        return context


class OrderHistoryView(ListView):
    paginate_by = 2
    template_name = 'accounts/order_history.html'
    model = Order

    @method_decorator(login_required(login_url="accounts:login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = Order.objects.filter(customer=self.request.user)
        context = super(OrderHistoryView, self).get_context_data(object_list=object_list, **kwargs)
        order = Order.objects.filter(customer=self.request.user)
        order_item = OrderItem.objects.filter(order__in=order)
        context['order'] = order
        context['order_item'] = order_item
        context['top_category'] = TopCategory.objects.all()
        context['cart'] = Cart(self.request)
        activities = self.get_related_activities(order)
        context['page_obj'] = activities
        return context

    def get_related_activities(self, order_history):
        paginator = Paginator(order_history, 2)  # paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities



class PasswordsResetView(PasswordResetView):
    form_class = PasswordsResetForm
    template_name = 'accounts/reset_password.html'
    email_template_name = 'accounts/password_reset_email.html'
    html_email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['top_category'] = TopCategory.objects.all()
        return context


class PasswordsResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['top_category'] = TopCategory.objects.all()
        return context


class PasswordsResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['top_category'] = TopCategory.objects.all()
        return context


class PasswordsResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['top_category'] = TopCategory.objects.all()
        return context


def success_registration(request):
    context = {
        'top_category': TopCategory.objects.all(),
        'cart': Cart(request)
    }
    return render(request, 'accounts/success_registration.html', context)


@login_required(login_url="accounts:login")
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url="accounts:login")
def account_detail(request):
    context = {
        'top_category': TopCategory.objects.all(),
        'cart': Cart(request)
    }
    return render(request, 'accounts/account.html', context)


@login_required(login_url="accounts:login")
def personal_data(request):
    context = {
        'top_category': TopCategory.objects.all(),
        'cart': Cart(request)
    }
    return render(request, 'accounts/account.html', context)


@login_required(login_url="accounts:login")
def order_history(request):
    order = Order.objects.filter(customer=request.user)
    order_item = OrderItem.objects.filter(order__in=order)
    print(f'{order_item} order_item')
    context = {
        'order': order,
        'order_item': order_item,
        'top_category': TopCategory.objects.all(),
        'cart': Cart(request)
    }
    return render(request, 'accounts/order_history.html', context)
