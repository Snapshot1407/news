from celery import shared_task
from time import sleep

@shared_task
def hello():
    sleep(10)
    print('Hello, world!')


@shared_task
def printer(N):
    for i in range(N):
        sleep(1)
        print(i+1)
