from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from django import forms
from datetime import date

from .models import Post, Author, Category


class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in [2023, 2024, 2025]]
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-{}'.format(year, month, day)


# создаём фильтр
class PostFilter(FilterSet):

    # def __init__(self, *args, **kwargs):
    #     self.form.fields['date__gt'].input_formats = ['%d-%m-%Y']

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
        # widget=forms.TextInput(attrs={'data-mask': "YYYY-MM-DD", 'placeholder': 'YYYY-MM-DD', })
        widget=DateSelectorWidget(),
    )
    author = ModelChoiceFilter(queryset=Author.objects.all(), label='Автор ',)
    categoriesPost = ModelChoiceFilter(queryset=Category.objects.all(), label='Категория ',)
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
