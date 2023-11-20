from django.core.management.base import BaseCommand, CommandError
from news.models import PostCategory


class Command(BaseCommand):
    help = 'Deletes all posts belongs to specified category'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        # self.stdout.readable()
        self.stdout.write(
            f'Do you really want to delete all posts belongs category {options["category"]}? yes/no')
        answer = input()

        if answer == 'yes':
            posts = PostCategory.objects.filter(category__name=options["category"])
            if len(posts) < 1:
                self.stdout.write(self.style.ERROR('There is nothing to delete!'))
                return
            posts.delete()
            self.stdout.write(self.style.SUCCESS('Succesfully posts has been deleted!'))
            return

        self.stdout.write(self.style.ERROR('Access denied'))
