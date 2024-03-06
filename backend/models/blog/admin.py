from django.contrib import admin
from .models import Article, Category
from mptt.admin import DraggableMTTAdmin

@admin.register(Category)
class CategoryAdmin(DraggableMTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {'fields': ('title', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)})
    )


admin.site.register(Article)