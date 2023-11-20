from django.core.management.base import BaseCommand, CommandError
from news.models import Subscribe


class Command(BaseCommand):
    help = "Delete all subscribers."

    def handle(self, *args, **options):
        Subscribe.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully delete!'))
