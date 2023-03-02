from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from accounts.managers import UserManager


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField("name", max_length=500)
    surname = models.CharField("surname", max_length=500)

    def __str__(self):
        return f"{self.name} {self.surname}"


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(_('first_name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('last_name'), max_length=255, null=True, blank=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    phone = models.CharField(_('phone number'), max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)

    is_verified = models.BooleanField(_('verified'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('username', 'email', 'phone')
