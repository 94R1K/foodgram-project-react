from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        db_index=True,
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )
    is_subscribed = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['id']

    def __str__(self):
        return f'Пользователь {self.username}'


User = CustomUser


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='Подписка',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow',
            )
        ]

    def __str__(self):
        return f'{self.user} follows {self.following}'
