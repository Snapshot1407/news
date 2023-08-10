from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'