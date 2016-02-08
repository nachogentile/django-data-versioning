from django.db import models


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
    scripts_version = models.CharField(max_length=500)

    def __str__(self):
        return self.name
