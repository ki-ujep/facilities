from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        failed = True
        while failed:
            try:
                db_conn = connections['default']
                cursor = db_conn.cursor()
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
            else:
                failed = False
        self.stdout.write(self.style.SUCCESS('Database available!'))
