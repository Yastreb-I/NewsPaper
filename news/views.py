from django.shortcuts import render
# from django.shortcuts import render
from django.views.generic import ListView, DetailView  # импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from .models import Post
from datetime import datetime


class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML,
    # в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-dateCreation')  # Вывод новых статей в начало страницы
    paginate_by = 5  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        # context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# создаём представление, в котором будут детали конкретного отдельного поста
class NewsDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'one_news.html'  # название шаблона
    context_object_name = 'one_news'  # название объекта
