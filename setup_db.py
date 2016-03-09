import subprocess
from django.conf import settings
from django.core.management.commands import migrate


def create_database(db_name):
    """
    Creates and populates a new database based on the name provided
    """
    subprocess.call(["createdb", "-U", "postgres", db_name, '-h', settings.PGSQL_SERVER_ADDRESS])
    migrate_cmd = migrate.Command()
    migrate_cmd.execute(database=db_name, app_label=None, interactive=False, verbosity=1)
