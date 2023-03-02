from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

from news.forms import *
from news.models import News
from news.utils import *

class NewsPage(DataMixin, ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'allnews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        unique_context = self.get_user_context(title='Новости', activenews='active')
        return dict(list(context.items())+list(unique_context.items()))


class CategoryNewsPage(DataMixin, ListView):
    model = News
    template_name = 'news/newscategory.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['name'] = Category.objects.values('name').get(slug=self.kwargs['category_slug'])['name']
        unique_context = self.get_user_context(title=f"Новости {context['name']}", activenews='active')
        return dict(list(context.items())+list(unique_context.items()))

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'])


class SearchPage(DataMixin, ListView):
    model = News
    template_name = 'news/search.html'
    context_object_name = 'allnews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f"text={self.request.GET.get('text')}&"
        unique_context = self.get_user_context(title='Поиск по сайту')
        return dict(list(context.items())+list(unique_context.items()))

    def get_queryset(self):  # новый
        query = self.request.GET.get('text')
        if query:
            return News.objects.filter(Q(title__icontains=query) |
                                       Q(description__icontains=query)).select_related('category') | News.objects.filter(category__name=query)
        return list()


class HomePage(DataMixin, TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Главная', activehome='active')
        return dict(list(context.items()) + list(unique_context.items()))


class ContactsPage(DataMixin, TemplateView):
    template_name = 'news/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Контакты', activeother='active')
        return dict(list(context.items()) + list(unique_context.items()))


class ProjectsPage(DataMixin, TemplateView):
    template_name = 'news/projects.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Проекты', activeother='active')
        return dict(list(context.items()) + list(unique_context.items()))


class AddNews(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddNewsForm
    template_name = 'news/addnews.html'
    success_url = reverse_lazy('news')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Добавить новости')
        return dict(list(context.items()) + list(unique_context.items()))


class LoginUser(DataMixin, LoginView):
    template_name = 'news/logon.html'
    success_url = reverse_lazy('home')
    form_class = LoginUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_context = self.get_user_context(title='Личный кабинет', activelogon='active')
        context['formone'] = context['form']
        context['formtwo'] = RegisterUserForm
        context['active1'] = 'active'
        context['act1'] = 'show active'
        return dict(list(context.items()) + list(unique_context.items()))


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

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

def login_or_reg(request):
    if request.POST:
        if 'password2' in request.POST:
            return RegisterUser.as_view()(request)
    return LoginUser.as_view()(request)

def logout_user(request):
    logout(request)
    return redirect('logon')

