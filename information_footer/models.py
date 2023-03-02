from django.db import models
from ckeditor.fields import RichTextField


class FooterText(models.Model):
    title = models.CharField(max_length=100, verbose_name="Ім'я статті")
    text = RichTextField(verbose_name='Опис', null=True, blank=True)
    slug = models.SlugField(verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Інформація у підвалі'
        verbose_name_plural = 'Інформація у підвалі'
