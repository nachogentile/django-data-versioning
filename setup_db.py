import logging
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
    engine_type = settings.DATABASES.get("default").get("ENGINE").split(".")[-1]

    if engine_type.find("postgresql") != -1:
        command = ["createdb", "-U", "postgres", db_name, '-h', settings.DB_SERVER_ADDRESS]
        subprocess.call(command)

    elif engine_type.find("mysql") != -1:
        import MySQLdb
        db = MySQLdb.connect(host=settings.DATABASES.get("default").get("HOST"),
                             user=settings.DATABASES.get("default").get("USER"),
                             passwd=settings.DATABASES.get("default").get("PASSWORD"))
        cur = db.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_name))

    elif engine_type.find("sqlite") != -1:
        pass
    else:
        logging.error("Database system %s is not available with data_versioning")

    migrate_db(db_name)
