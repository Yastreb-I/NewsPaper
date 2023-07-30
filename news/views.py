from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView  # импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.cache import cache

import logging

from .models import Post, Category, Author
from .filters import PostFilter  # импортируем свой фильтр
from .forms import PostForm

logger_dj = logging.getLogger('django')
# logger_dj_req = logging.getLogger('django.request')


class NewsList(ListView):

    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML,
    # в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-dateCreation')  # Вывод новых статей в начало страницы
    paginate_by = 5  # поставим постраничный вывод в 5 элемента

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        user = self.request.user
        categorise = Category.objects.all()
        subsc_list = []
        try:
            context['is_not_group_author'] = not self.request.user.groups.filter(name='authors').exists()
            # registered_user = self.request.user.groups.filter(name='common').exists()
            if user.is_authenticated:
                for category in categorise:
                    if category.subscribers.filter(email=user.email).exists():
                        subsc_list.append(category.id)
            context['cat_sub'] = subsc_list
        except Exception as e:
            logger_dj.exception(e)

        return context


# создаём представление, в котором будут детали конкретного отдельного поста
class NewsDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретной отдельной новости
    template_name = 'one_news.html'  # название шаблона
    context_object_name = 'one_news'  # название объекта

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'{self.kwargs["pk"]}', obj)
        return obj


class SearchPost(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр
        context['is_not_group_author'] = not self.request.user.groups.filter(name='authors').exists()

        user = self.request.user
        categorise = Category.objects.all()
        subsc_list = []
        if user.is_authenticated:
            for category in categorise:
                if category.subscribers.filter(email=user.email).exists():
                    subsc_list.append(category.id)
        context['cat_sub'] = subsc_list
        return context


# Дженерик для создания объекта. Надо указать только имя шаблона и класс формы
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        groups_authors = user.groups.filter(name='authors').exists()
        # Кол-во постов автора в день
        if groups_authors:
            day = datetime.today().strftime("%Y-%m-%d")
            author = Author.objects.get(userAuthor__id=user.id)
            post_to_day = Post.objects.filter(author=author, dateCreation__date=day).count()
            context['post_to_day'] = post_to_day
        context["test"] =self.request.path
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, user)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый пост
            post = form.save()
            post.author = Author.objects.get_or_create(userAuthor=user)[0]
            form.save()
            return self.form_valid(form)

        return redirect("news:news")


# Дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)
    success_url = '/news/'

    # login_url = '/accounts/login/'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
    # который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    permission_required = ('news.delete_post',)
    queryset = Post.objects.all()
    success_url = '/'

    def get_success_url(self):
        return f'/news/'

