from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from news.forms import *
from news.models import News
from news.permissions import IsAdminOrReadOnly, IsUserOrReadOnly
from news.serializers import NewsSerializer
from news.utils import *


# Класс для новостей на странице
class NewsPage(DataMixin, ListView):

    # Подключаем модель News
    model = News

    template_name = 'news/news.html'
    context_object_name = 'allnews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Создаём объект для выбора категорий на странице
        context['category'] = Category.objects.all()

        unique_context = self.get_user_context(title='Новости', activenews='active')
        return dict(list(context.items())+list(unique_context.items()))

# Класс для новостей на странице, отфильтрованных по определённой категории
class CategoryNewsPage(DataMixin, ListView):

    # Подключаем модель News
    model = News

    template_name = 'news/newscategory.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Создаём объект для выбора категорий на странице
        context['category'] = Category.objects.all()

        # Вытаскиваем наименование категории
        context['name'] = Category.objects.values('name').get(slug=self.kwargs['category_slug'])['name']

        unique_context = self.get_user_context(title=f"Новости: {context['name']}", activenews='active')
        return dict(list(context.items())+list(unique_context.items()))

    # Получаем список из новостей по выбранной категории
    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'])


# Класс для результатов поиска
class SearchPage(DataMixin, ListView):

    # Подключаем модель News
    model = News

    template_name = 'news/search.html'
    context_object_name = 'allnews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текст, который ввёл пользователь, чтобы вставить его в ссылку
        context['text'] = f"text={self.request.GET.get('text')}&"

        unique_context = self.get_user_context(title='Поиск по сайту')
        return dict(list(context.items())+list(unique_context.items()))

    # Получаем список из новостей, которые удовлетворяют поисковому запросу
    def get_queryset(self):  # новый
        query = self.request.GET.get('text')
        if query:
            return News.objects.filter(Q(title__icontains=query) |
                                       Q(description__icontains=query)).select_related('category') | News.objects.filter(category__name=query)
        return list()

# Класс для главной страницы
class HomePage(DataMixin, TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Главная', activehome='active')
        return dict(list(context.items()) + list(unique_context.items()))

# Класс для страницы с контактами
class ContactsPage(DataMixin, TemplateView):
    template_name = 'news/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Контакты', activeother='active')
        return dict(list(context.items()) + list(unique_context.items()))

# Класс для страницы с проектами
class ProjectsPage(DataMixin, TemplateView):
    template_name = 'news/projects.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Проекты', activeother='active')
        return dict(list(context.items()) + list(unique_context.items()))

# Класс для страницы добавления новостей
# LoginRequiredMixin позволяет перейти на страницу только авторизованным пользователям
class AddNews(DataMixin, LoginRequiredMixin, CreateView):

    # Подключаем форму для добавления новостей
    form_class = AddNewsForm

    template_name = 'news/addnews.html'
    success_url = reverse_lazy('news')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Добавить новости')
        return dict(list(context.items()) + list(unique_context.items()))

# Класс для авторизации пользователей, используется в методе login_or_reg
class LoginUser(DataMixin, LoginView):
    template_name = 'news/logon.html'
    success_url = reverse_lazy('home')

    # Подключаем форму для авторизации
    form_class = LoginUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Личный кабинет', activelogon='active')
        context['formone'] = context['form']
        context['formtwo'] = RegisterUserForm
        context['active1'] = 'active'
        context['act1'] = 'show active'
        return dict(list(context.items()) + list(unique_context.items()))

# Класс для регистрации пользователей, используется в методе login_or_reg
class RegisterUser(DataMixin, CreateView):
    template_name = 'news/logon.html'
    success_url = reverse_lazy('home')
    form_class = RegisterUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Личный кабинет', activelogon='active')
        context['formone'] = LoginUserForm
        context['formtwo'] = context['form']
        context['active2'] = 'active'
        context['act2'] = 'show active'
        return dict(list(context.items()) + list(unique_context.items()))

    # Если регистрация прошла успешно, то сразу авторизовываем пользователя сайте
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

# Метод для страницы с авторизацией и регистрацией - определяет, какую именно форму возвращать
def login_or_reg(request):
    if request.POST:
        if 'password2' in request.POST:
            return RegisterUser.as_view()(request)
    return LoginUser.as_view()(request)

# Метод для выхода из профиля
def logout_user(request):
    logout(request)
    return redirect('logon')

# API для вывода первых 5 новостей и добавления новости
class NewsAPIView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    # Вносить записи могут только авторизованные
    # permission_classes = (IsAuthenticatedOrReadOnly, )

    # Создавать записи могут только авторизованные по токену
    authentication_classes = (TokenAuthentication, )

# API обновления конкретной записи
class NewsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    # Обновлять запись могут только создатели записи или администратор
    permission_classes = (IsUserOrReadOnly,)

class NewsAPIDestroyView(generics.RetrieveDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    # УДалить запись может только администратор
    permission_classes = (IsAdminOrReadOnly,)

#
# class NewsViewSet(viewsets.ModelViewSet):
#     #queryset = News.objects.all()
#     serializer_class = NewsSerializer
#
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#
#         if not pk:
#             return News.objects.all()[:3]
#         return News.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'category': cats.name})
#
#     permission_classes = (IsAuthenticatedOrReadOnly, )