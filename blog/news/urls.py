from django.urls import path

from news.views import *

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
    path('search/', SearchPage.as_view(), name='search')]
