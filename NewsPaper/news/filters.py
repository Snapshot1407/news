from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Post, Author
from django import forms

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    name = CharFilter(field_name='title',
                      label="Название",
                      lookup_expr='icontains')
    author = ModelChoiceFilter(field_name='author',
                               queryset= Author.objects.all(),
                               label="Автор", empty_label ='любой')
    date = DateFilter(field_name='time_in',
                      widget=forms.DateInput(attrs={'type': 'date'}),
                      lookup_expr='gt',
                      label='Поиск по дате начиная с')
    class Meta:
        model = Post
        fields = [
            'name','author','date'
        ]
