from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from .models import Post
from .filters import PostFilter  # импортируем фильтр
from .forms import PostForm


class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML,
    # в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-dateCreation')  # Вывод новых статей в начало страницы
    paginate_by = 3  # поставим постраничный вывод в 2 элемента

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        # context['filter'] = PostFilter(self.request.GET,
        #                                   queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


# создаём представление, в котором будут детали конкретного отдельного поста
class NewsDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретной отдельной новости
    template_name = 'one_news.html'  # название шаблона
    context_object_name = 'one_news'  # название объекта


class SearchPost(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр
        return context


# Дженерик для создания объекта. Надо указать только имя шаблона и класс формы
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


# Дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

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

