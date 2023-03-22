from django.urls import path, include, re_path
from rest_framework import routers

from news.views import *

# Попытка создат роутер
# router = routers.SimpleRouter()
# router.register(r'news', NewsViewSet, basename='news')
# print(router.urls)

# Создаём ссылки и зависимости для приложения News
urlpatterns = [
    # Главная страница
    path('', HomePage.as_view(), name='home'),
    # Страница с новостями
    path('news/', NewsPage.as_view(), name='news'),
    # Страница с новостями по категории, добавляем slug с названием категории в ссыллку
    path('news/<slug:category_slug>/', CategoryNewsPage.as_view(), name='category'),
    # Страница с контактами
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    # Страница с проектами
    path('projects/', ProjectsPage.as_view(), name='projects'),
    # Страница авторизации и регистрации
    path('logon/', login_or_reg, name='logon'),
    # Страница для выхода из профиля
    path('logout/', logout_user, name='logout'),
    # Страница для добавления новостей (только для администратора)
    path('addnews/', AddNews.as_view(), name='addnews'),
    # Страница с результатами поиска
    path('search/', SearchPage.as_view(), name='search'),
    # API для аутентификации пользователя через токе
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # API для аутентификации пользователя на сайте через cookies
    path('api/v1/authsesseion/', include('rest_framework.urls')),
    # API для получения списка новостей и добавления новости
    path('api/v1/news/', NewsAPIView.as_view()),
    # API для просмотра/обновления какой-либо новости
    path('api/v1/news/<int:pk>/', NewsAPIUpdate.as_view()),
    # API для просмотра/удаления новости
    path('api/v1/newsdelete/<int:pk>/', NewsAPIDestroyView.as_view())
]