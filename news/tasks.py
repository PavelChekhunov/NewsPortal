from celery import shared_task
import datetime
from .models import Post
from .tools import send_email


@shared_task
def newsletter(post_id):
    post_q = Post.objects.filter(pk=post_id)
    if post_q and len(post_q) > 0:
        post = post_q[0]
        categories = post.category.values_list('pk', flat=True)
        send_email(f'Новость: {post.title}', post, list(categories))


@shared_task
def newsletters():
    today = datetime.datetime.now()
    days_ago = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(datetime_created__gte=days_ago)
    if posts and len(posts) > 0:
        categories_id = set(posts.values_list('category__pk', flat=True))
        title = 'Уведомление. Рассылка новостей за неделю.'
        send_email(title, posts, categories_id)
