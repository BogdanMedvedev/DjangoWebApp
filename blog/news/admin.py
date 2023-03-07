# Настраиваем отображение в админ-панели

from django.contrib import admin

from .models import *

# Класс для отображения модели News
class NewsAdmin (admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'time_update')
    search_fields = ('title', 'description')

# Класс для отображения модели Category
class CategoryAdmin (admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}

# Сопоставляем описанные выше классы с соответствующими моделями
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)


