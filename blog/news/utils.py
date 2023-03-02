menu = {'Главная': 'Главная', 'Новости': 'Новости', 'Интересное': 'Интересное',
        'Контакты': 'Контакты', 'Проекты': 'Мои проекты', 'Something': 'Something else here',
        'logon': 'Личный кабинет'}


class DataMixin:
    paginate_by = 6

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
