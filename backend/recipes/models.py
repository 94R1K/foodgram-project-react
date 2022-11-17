from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag
from users.models import CustomUser

User = CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='backend_media/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientsInRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
        null=False,
        blank=False
    )
    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        verbose_name='Хештег',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
        related_name='ingredients_list',
        null=False,
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты',
        related_name='ingredient_in_recipe',
        null=False,
        blank=False
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов',
        null=False,
        blank=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')
        ]
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='users_favorites',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='favorite_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} added {self.recipe.name} to favorite'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Список покупок',
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Покупка',
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='shoppinglist_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} added {self.recipe} in shopping cart'
