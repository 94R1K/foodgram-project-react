from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag
from users.models import CustomUser

User = CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='media/',
        null=False,
        default=None,
        verbose_name='Изображение'
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='ingredients'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Хэштег',
        related_name='tags'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        related_name='ingredient_amounts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_amounts'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')
        ]
        verbose_name = 'Количество'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления в избранное'
    )

    class Meta:
        verbose_name_plural = 'Избранные'
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='favorite_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe.name}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='user_shopping_list',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Покупка',
        related_name='purchases',
        on_delete=models.CASCADE
    )
    added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления в список покупок'
    )

    class Meta:
        verbose_name_plural = 'Покупки'
        verbose_name = 'Покупка'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='shoppinglist_unique'
            )
        ]

    def __str__(self):
        return f'У {self.user} в списке покупок: {self.recipe}'
