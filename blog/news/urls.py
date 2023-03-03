from django.urls import path

from news.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('news/', NewsPage.as_view(), name='news'),
    path('news/<slug:category_slug>/', CategoryNewsPage.as_view(), name='category'),
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    path('projects/', ProjectsPage.as_view(), name='projects'),
    path('logon/', login_or_reg, name='logon'),
    path('logout/', logout_user, name='logout'),
    path('addnews/', AddNews.as_view(), name='addnews'),
    path('search/', SearchPage.as_view(), name='search')]
