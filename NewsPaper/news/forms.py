from django.forms import ModelForm, CharField

from .models import Post


class PostForm(ModelForm):
    title = CharField(label='Название')
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author','category',
        ]

        labels = {
            'author' : 'Автор',
            'category' : 'Категория'
        }