from django.db import models


class Tag(models.Model):
    name = models.CharField(
        'Имя тега',
        max_length=128,
        unique=True
        )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True
        )
    slug = models.CharField(
        'Ссылка',
        max_length=128,
        unique=True
        )

    def __str__(self):
        return self.name
