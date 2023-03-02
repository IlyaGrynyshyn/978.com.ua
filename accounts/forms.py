from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.forms import TextInput

from accounts.models import User


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'E-mail или телефон',
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(phone=username).exists():
                if not User.objects.filter(email=username).exists():
                    raise forms.ValidationError(f'Невірний логін або пароль')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Невірний логін або пароль")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'email': TextInput(attrs={'placeholder': 'Ваш Email', 'type': 'text'}),
            'password': TextInput(attrs={'placeholder': 'Ваш пароль'})
        }


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': '+38(___)___-____'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Ваша пошта', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Електронна пошта'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Підтвердити пароль'
        self.fields['first_name'].label = 'Ім\'я'
        self.fields['phone'].label = 'Номер телефону'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f'Дана пошта вже зареєстрована'
            )
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                f'Даний номер телефону вже зареєстрований'
            )
        return phone

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'first_name', 'phone', 'password', 'confirm_password']
        widgets = {
            'email': TextInput(attrs={'placeholder': 'Ваш Email', 'type': 'email'}),
            'password': TextInput(attrs={'placeholder': 'Ваш пароль'}),
            'confirm_password': TextInput(attrs={'placeholder': 'Підтвердіть пароль'}),
            'first_name': TextInput(attrs={'placeholder': 'Ваше ім\'я'}),
            'phone': TextInput(attrs={'placeholder': 'Номер телефону'})
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.PasswordInput(attrs={'type': 'password'})
    new_password1 = forms.PasswordInput(attrs={'type': 'password'})
    new_password2 = forms.PasswordInput(attrs={'type': 'password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Старий пароль'
        self.fields['new_password1'].label = 'Новий пароль'
        self.fields['new_password2'].label = 'Підтвердіть пароль'

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class PasswordsResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f'Дана пошта не зареєстрована'
            )
        return email

    class Meta:
        model = User
        fields = '__all__'
