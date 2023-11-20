from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tools import send_email


@receiver(m2m_changed, sender=Post.category.through)
def notify_post_added(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add':
        return
    subject = f'Новость: {instance.title}'
    send_email(subject, instance, pk_set)
