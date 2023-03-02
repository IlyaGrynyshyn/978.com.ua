
from django.forms.widgets import Widget
from django.shortcuts import render


class DeliveryFormFieldWidget(Widget):

    template_name = 'delivery/form.html'

    def __init__(self, *args, **kwargs):
        self.form = None
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['form'] = self.form
        return context


