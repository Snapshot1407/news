from celery import shared_task
from time import sleep
import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.utils import timezone


from .models import Category, Post


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    title = post.title
    subscribers_email = []

    for c in categories:
        subscribers_user = c.subscribers.all()
        for s_u in subscribers_user:
            subscribers_email.append(s_u.email)

    html_content = render_to_string(
        'subscribe/post_created.html',
        {
            'text': post.preview,
            'link': f'http://127.0.0.1:8000/NewsPortal/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'subscribe/daily_post.html',
        {
            'link': f'http://127.0.0.1:8000/NewsPortal/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
