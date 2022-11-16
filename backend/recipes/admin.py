from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientsInRecipe, Recipe,
                     ShoppingCart)


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe__name', 'ingredient__name')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInRecipeInline,)
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
    )
    search_fields = (
        'name',
        'author__username',
        'author__email'
    )
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('is_favorited',)

    def is_favorited(self, instance):
        return instance.favorite_recipes.count()


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(IngredientsInRecipe, IngredientsInRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
