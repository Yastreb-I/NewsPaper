from django.urls import path
from .views import NewsList, NewsDetail, SearchPost, PostCreateView  # импортируем наше представление
from .views import PostUpdateView, PostDeleteView

from django.views.decorators.cache import cache_page


urlpatterns = [
    # path — означает путь.
    # path('', cache_page(60)(NewsList.as_view()), name="news"), # кеширование главной страницы
    path('', NewsList.as_view(), name="news"),
    path('search', SearchPost.as_view(), name="search"),
    path('<int:pk>', cache_page(60*5)(NewsDetail.as_view()), name="one_news"),  # pk — это первичный ключ новости,
    # который будет выводиться у нас в шаблон
    path('post_add', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание статьи
    path('post_update/<int:pk>', PostUpdateView.as_view(), name="post_update"),  # Ссылка на редактирование статьи
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name="post_delete"),  # Ссылка на удаление статьи



]