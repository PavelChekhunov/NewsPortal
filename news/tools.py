from django.core.mail import EmailMultiAlternatives
from .models import Category, Post
from django.conf import settings


def _get_recipients(categories):
    recipients = {}
    for cat in Category.objects.filter(pk__in=categories):
        for user in cat.subscribers.all():
            recipients[user.username] = user.email
    print(recipients)
    return recipients


def _get_html_content(posts):
    full_path = f'{settings.SITE_URL}/posts/'
    if isinstance(posts, Post):
        html_message = '<br />Вы получили это письмо так как подписаны на рассылку.<br /><br />'
        text = posts.text.replace('\n', '<br />')[:50]
        html_message += f"<br />{posts.title}</br /><br />{text}<br /> <br /><br />"
        html_message += f'\n<a href="{full_path}{posts.pk}">Перейти на страницу статьи</a>\n'
    else:
        html_message = '<br />Новости за неделю.<br /><br />'
        for post in posts:
            html_message += f'\n<br /><a href="{full_path}{post.pk}">{post.title}</a><br />\n'
    return html_message


def send_email(subject, posts, categories_id):
    recipients = _get_recipients(categories_id)
    if len(recipients) < 1:
        return
    html_message = _get_html_content(posts)
    for k, v in recipients.items():
        html_message = f'<p><h3>Здравствуйте {k}!</h3></p>{html_message}'
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
            to=[v]
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()


def send_email_notification(request, posts):
    post = request.POST
    send_email(post.get('title'), posts, post.get('category'))


def page_videos():
    return {
        135: "https://www.youtube.com/embed/4517pI-Evts",
        136: "https://www.youtube.com/embed/wZnVQT_iEYo",
        137: "https://www.youtube.com/embed/52DX9IPyBB8",
        139: "https://www.youtube.com/embed/wVFKAqDyohQ",
        154: "https://www.youtube.com/embed/YUFXalD-eY8",
        155: "https://www.youtube.com/embed/8LhkyyCvUHk",
        173: "https://www.youtube.com/embed/KyTIui1zyt4",
        204: "https://www.youtube.com/embed/pnyfESsYbYc",
        205: "https://www.youtube.com/embed/ticTtMXnnC8",
        206: "https://www.youtube.com/embed/jexG70VOfqM",
        207: "https://www.youtube.com/embed/qbSxck-b1Cs",
    }
