from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)


    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(result=Sum('rating')).get('result')
        comments_rating = Comment.objects.filter(user=self.user).aggregate(result=Sum('rating')).get('result')
        comment_post = Comment.objects.filter(post__author__user=self.user).aggregate(result=Sum('rating')).get('result')

        self.rating = (posts_rating * 3 +comments_rating + comment_post)
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = "AR"
    news = "NW"

    TYPE = [
        (article,'Статья'),
        (news,'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,choices=TYPE,default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category,through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


    def preview(self, len=124):
        return f"{self.text[:len]}..." if len(self.text) > len else self.text

    def __str__(self):
        return self.title.title()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



