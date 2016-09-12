Installation
============

In order to use the versioning system follow these steps:

- First of all, add 'data_versioning' to the INSTALLED_APPS list in your Django
  project settings.py.

- Change your database settings specification in order to look like this:

```python
from data_versioning.dynamic_db_dict import DynamicDbDict

DATABASES = DynamicDbDict({
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database/db.sqlite3'),
    }
})
```

- In order to allow the admin to display the user selected database, use the ModelAdmin
  class provided with this package, like in the example below:

```python
class CarGroupAdmin(DynamicDbAdmin):
    fields = ["name", ]
    list_display = ["name", ]
    filter_horizontal = []

admin.site.register(CarGroup, CarGroupAdmin)
```

- In order to perform migrate command on all the databases available, run the command "migrate_all" as following:

```python
./manage.py migrate_all
```

