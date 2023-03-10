from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

# Форма для добавления новостей в базу данных, используется во view AddNews
class AddNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Задаём поле на случай, если категория не выбрана
        self.fields['category'].empty_label = 'Категория не выбрана'

    # Связываем форму с моделью News и указываем, какие поля отображать на странице
    class Meta:
        model = News
        fields = ['title', 'description', 'url', 'photo', 'is_published', 'category']

    # Создаём собственный валидатор на случай, если длина заголовка больше 200 символов
    def clean_title(self):
        #Получаем данные в загаловке
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError ('Длина превышаем 200 символов')
        return title

# Форма для регистрации пользователей, используется во view RegisterUser
class RegisterUserForm(UserCreationForm):

    # Связываем форму с моделью News и указываем, какие поля отображать на странице
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

# Форма для авторизации пользователей, используется во view LoginUser
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

