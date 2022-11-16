from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Имя тега'
    )
    color = ColorField(
        max_length=8,
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Ссылка'
    )

    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'

    def __str__(self):
        return self.name
