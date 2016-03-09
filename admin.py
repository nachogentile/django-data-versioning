from django.contrib import admin
from data_versioning.models import DataVersion, UserDataVersion

admin.site.register(DataVersion)
admin.site.register(UserDataVersion)
