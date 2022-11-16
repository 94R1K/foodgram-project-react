from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    search_fields = ('name', 'color', 'slug')
    list_editable = ('color', )
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
