from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/", verbose_name='Фото')
    url = models.URLField(unique=True, verbose_name='Ссылка')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    is_published = models.BooleanField(default=True, verbose_name='Отображение')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['time_create']

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории новостей'
        verbose_name_plural = 'Категории новостей'
        ordering = ['id', 'name']

