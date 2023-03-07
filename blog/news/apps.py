from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # Название приложения для отображения в админ-панели
    verbose_name = 'Приложение для показа новостей'
