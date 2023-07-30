from django_filters import FilterSet, DateFilter, ModelChoiceFilter, \
    CharFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from django import forms
from datetime import date

from .models import Post, Author, Category


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


# создаём фильтр
class PostFilter(FilterSet):
    # def __init__(self, *args, **kwargs):
    #     self.form.fields['date__gt'].input_formats = ['%d-%m-%Y']

    headPost = CharFilter(
        label='Заголовок',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите заголовок статьи',
            'class': 'filter_form_head',
            }))

    dateCreation = DateFilter(label='Поиск статьи с ',
                              lookup_expr='gte',
                              # required=True,
                              widget=MyDateInput({
                                  'class': 'filter_form_date',
                                  # 'value': "2023-06-01",
                              }))

    author = ModelChoiceFilter(queryset=Author.objects.all(),
                               label='Автор ',
                               widget=forms.Select({
                                   'class': 'filter_form_author',
                               }))

    categoriesPost = ModelChoiceFilter(queryset=Category.objects.all(),
                                       label='Категория ',
                                       widget=forms.Select({
                                           'class': 'filter_form_category'
                                       }))

    # Здесь в мета классе надо предоставить модель и указать поля,
    # по которым будет фильтроваться (т.е. подбираться) информация о статьях

    class Meta:
        model = Post
        fields = ('headPost',
                  'dateCreation',
                  'author',
                  'categoriesPost',
                  )  # поля, которые мы будем фильтровать
        # (т.е. отбирать по каким-то критериям, имена берутся из моделей)
