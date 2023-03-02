from django.urls import path
from django.views.decorators.cache import cache_page

from news.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('news/', cache_page(300)(NewsPage.as_view()), name='news'),
    path('news/<slug:category_slug>/', cache_page(300)(CategoryNewsPage.as_view()), name='category'),
    path('contacts/', cache_page(300)(ContactsPage.as_view()), name='contacts'),
    path('projects/', ProjectsPage.as_view(), name='projects'),
    path('logon/', login_or_reg, name='logon'),
    path('logout/', logout_user, name='logout'),
    path('addnews/', AddNews.as_view(), name='addnews'),
    path('search/', SearchPage.as_view(), name='search')]
