# from django import template
# from django.db.models import Q
#
# from news.forms import LoginUserForm, RegisterUserForm
# from news.models import *
#
# register = template.Library()

#Тег для отображения списка новостей
# @register.inclusion_tag('news/list_news.html')
# def get_news():
#     news_list = {'news': News.objects.all()}
#     return news_list

# @register.simple_tag(name='category')
# def get_category(filter=None):
#     return Category.objects.filter(~Q(sulg=filter))




