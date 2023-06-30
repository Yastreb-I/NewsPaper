from django.urls import path
from .views import NewsList, NewsDetail, SearchPost, PostCreateView  # импортируем наше представление
from .views import PostUpdateView, PostDeleteView
urlpatterns = [
    # path — означает путь.
    path('', NewsList.as_view(), name="news"),
    path('search', SearchPost.as_view(), name="search"),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    path('<int:pk>', NewsDetail.as_view(), name="one_news"),  # pk — это первичный ключ новости,
    # который будет выводиться у нас в шаблон
    path('post_add', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание статьи
    path('post_update/<int:pk>', PostUpdateView.as_view(), name="post_update"),  # Ссылка на редактирование статьи
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name="post_delete"),  # Ссылка на удаление статьи
]