# import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# from news.models import Post
# from news.tools import send_email


logger = logging.getLogger(__name__)


# def job_notify_byemail():
#     today = datetime.datetime.now()
#     days_ago = today - datetime.timedelta(days=7)
#     posts = Post.objects.filter(datetime_created__gte=days_ago)
#     if posts and len(posts) > 0:
#         categories_id = set(posts.values_list('category__pk', flat=True))
#         title = 'Уведомление. Рассылка новостей за неделю.'
#         send_email(title, posts, categories_id)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # scheduler.add_job(
        #     job_notify_byemail,
        #     trigger=CronTrigger(day_of_week="sat", hour="21", minute="33"),
        #     id="job_notify_byemail",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added job 'job_notify_byemail'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="sat", hour="19", minute="40"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
