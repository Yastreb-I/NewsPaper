from django.urls import path
from .views import NewsList, NewsDetail  # импортируем наше представление

urlpatterns = [
    # path — означает путь.
    path('', NewsList.as_view(), name="news"),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    path('<int:pk>', NewsDetail.as_view()),  # pk — это первичный ключ новости,
    # который будет выводиться у нас в шаблон
]