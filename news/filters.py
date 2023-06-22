from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from django import forms
from .models import Post, Author


# создаём фильтр
class PostFilter(FilterSet):
    headPost = CharFilter(
        label='Заголовок',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите заголовок статьи',
            'style': "width: 60vw;",
        }))
    dateCreation = DateFilter(
        label='Поиск статьи с ',
        lookup_expr='gte',
        # input_formats=['%d.%m.%Y'],
        widget=forms.TextInput(attrs={'data-mask': "YYYY-MM-DD", 'placeholder': 'YYYY-MM-DD', })
    )
    author = ModelChoiceFilter(queryset=Author.objects.all(), label='Автор ',)

    # Здесь в мета классе надо предоставить модель и указать поля,
    # по которым будет фильтроваться (т.е. подбираться) информация о статьях
    class Meta:
        model = Post
        fields = ('headPost',
                  'dateCreation',
                  'author',
                  )  # поля, которые мы будем фильтровать
        # (т.е. отбирать по каким-то критериям, имена берутся из моделей)
