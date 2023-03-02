# Generated by Django 4.1.6 on 2023-02-27 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_news_options_category_slug_alter_news_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=250, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=250, unique=True, verbose_name='URL'),
        ),
    ]
