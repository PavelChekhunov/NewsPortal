from django.core.management.base import BaseCommand, CommandError
import logging


class Command(BaseCommand):
    help = "Run loggers with all levels of the messages"

    def add_arguments(self, parser):
        parser.add_argument('loggers', type=str)

    def handle(self, *args, **options):
        logs = options['loggers']
        if logs:
            loggers = logs.replace(',', ' ').split()
        else:
            loggers = ('django', 'django.request', 'django.server', 'django.template', 'django.db.backends',
                       'django.security')
        for logger in [logging.getLogger(name) for name in loggers]:
            logger.info(f"Logger: {logger.name}")
            logger.debug('testlog DEBUG message')
            logger.info('testlog INFO message')
            logger.warning('testlog WARNING message')
            logger.error('testlog ERROR message')
            logger.critical('testlog CRITICAL message')
