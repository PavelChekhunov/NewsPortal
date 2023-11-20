import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Лень разбираться как сделать так, чтобы задача работала на локальном времени.
# В учебном материале нет ничего по данному поводу.
# Задача настроена на исполнение по Московскому времени +3
# Для других часовых поясов необходимо изменить параметр CELERY_TIMEZONE в settings.py
# Или в settings.py убрать CELERY_ENABLE_UTC и CELERY_TIMEZONE и
# для срабатывания задачи по локальному времени необходимо вычесть разницу по времени часового пояса
# и времени по Гринвичу в параметре schedule
app.conf.beat_schedule = {
    'newsletters_every_monday_8am': {
        'task': 'news.tasks.newsletters',
        'schedule': crontab(day_of_week='1', hour="8", minute="0"),
        'args': (),
    },
}
