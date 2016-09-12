from django.db import models

from data_versioning.setup_db import create_database


class UserDataVersion(models.Model):
    """
    Specify the data version that the user is currently using.
    """
    user = models.OneToOneField("auth.User")
    current_version = models.ForeignKey("DataVersion")

    def __str__(self):
        return "{} using {}".format(self.user.username, self.current_version.name)


class DataVersion(models.Model):
    """
    Each data version is linked to both a version of the scripts and a specific database.
    """
    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.replace(' ', '_')
        super(DataVersion, self).save()
        create_database(self.name)
