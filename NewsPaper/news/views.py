from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, resolve
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .tasks import send_email_task
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm


from django.views.decorators.cache import cache_page
from django.core.cache import cache
# Create your views here.
@cache_page(60*15)
class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'news_all'
    paginate_by = 10

    #@cache_page(60 * 15)
    def get_queryset(self):
        # self.category =get_object_or_404(Category, id=self.kwargs['pk'])
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
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}',obj)
        return obj

@cache_page(60 * 15)
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
        send_email_task.delay(post.pk)
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


@cache_page(60 * 15)
class PostCategoryView(ListView):
    model = Post
    template_name = 'subscribe/category.html'
    context_object_name = 'posts'
    ordering = '-time_create'
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['category'] = category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe/subscribed.html', {'category':category, 'message':message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect('/')



@cache_page(60 * 15)
class CategoryListView(ListView):
    model = Post
    template_name = 'subscribe/category_list.html'
    context_object_name = 'category_news_list'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is not subscriber'] = not self.category.subscribers.filter(id=self.request.user.id).exists()
        context['is_not_subscriber'] = self.request.user not in self.categories.subscribers.all()
        context['category'] = self.categories
        return context


    def get_queryset(self):
        self.categories =get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-time_create')
        return queryset
