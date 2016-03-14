import subprocess
from django.conf import settings
from django.core.management.commands import migrate


def migrate_db(db_name):
    """
    Launch migration command for the provided database name.
    """
    migrate_cmd = migrate.Command()
    migrate_cmd.execute(database=db_name, app_label=None, interactive=False, verbosity=1)


def create_database(db_name):
    """
    Creates and populates a new database based on the name provided.
    """
    subprocess.call(["createdb", "-U", "postgres", db_name, '-h', settings.PGSQL_SERVER_ADDRESS])
    migrate_db(db_name)
