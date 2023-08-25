from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.


   path('', PostsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]
