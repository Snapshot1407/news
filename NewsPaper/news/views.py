from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


from .models import Post
from .filters import PostFilter
from .forms import PostForm

# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context

# Добавляем новое представление для создания товаров.

class PostCreate(CreateView, PermissionRequiredMixin):
    permission_required = ('news.add_post',)

    form_class = PostForm
    context_object_name = 'post_create'
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/news/create/':
            post.post_type = 'NW'
        print(self.request.path)
        post.save()
        return super().form_valid(form)
class PostUpdate(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = ('news.change_post',)

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')



class PostDelete(DeleteView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

