
from django.core.management.base import BaseCommand, CommandError

from data_versioning.models import DataVersion
from data_versioning.setup_db import migrate_db
from entities.code_generation import makemigrations


class Command(BaseCommand):
    help = 'Migrate data structure for all database versions.'

    def handle(self, *args, **options):
        makemigrations_cmd = makemigrations.Command()
        makemigrations_cmd.execute(app_label=None, interactive=False, verbosity=1)

        migrate_db('default')

        try:
            for data_version in DataVersion.objects.all():
                migrate_db(data_version.name)
                self.stdout.write(self.style.SUCCESS('Successfully synced database {}'.format(data_version.name)))
        except Exception as e:
            raise CommandError('Can\'t synchronize databases: {}'.format(str(e)))
