

class DynamicDbDict(dict):
    def __init__(self, initial_data):
        self.update(initial_data)
        self._data = initial_data

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        try:
            from data_versioning.models import DataVersion
            dv = DataVersion.objects.get(name=key)
            copy = self._data['default'].copy()
            copy.update({
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'database/{}.sqlite3'.format(dv.name)
            })
            self._data[key] = copy
            return copy
        except Exception as e:
            print(e)

