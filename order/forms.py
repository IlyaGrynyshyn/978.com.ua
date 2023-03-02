from django import forms
from django.utils.translation import gettext_lazy as _

from delivery.fields import DeliveryFormField
from delivery.models import DeliveryMethod
from order.models import Order, DELIVERY_TYPE


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'class': 'required', 'placeholder': 'Введіть ім\'я'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'}))
    midl_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть '
                                                                                                      'по-батькові'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': '+38(___)___-____'}))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form__group'}))
    delivery = DeliveryFormField()

    # call_back = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "Ім'я"
        self.fields['first_name'].empty_label = "Обов'язкове для заповнення"
        self.fields['last_name'].label = 'Прізвище'
        self.fields['last_name'].empty_label = "Обов'язкове для заповнення"
        self.fields['midl_name'].label = 'По-батькові'
        self.fields['phone'].label = 'Номер телефону'
        self.fields['phone'].empty_label = "Обов'язкове для заповнення"
        self.fields['email'].label = "E-mail"
        self.fields['comment'].label = 'Коментарій до замовлення'
        self.fields['delivery'].init_form(*args, **kwargs)

    class Meta:
        model = Order
        fields = 'first_name', 'last_name', 'midl_name', 'phone', 'email', 'comment'
