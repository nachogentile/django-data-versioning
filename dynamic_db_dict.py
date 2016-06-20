

class DynamicDbDict(dict):
    def __init__(self, initial_data):
        self.update(initial_data)
        self._data = initial_data

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        try:
            from data_versioning.models import DataVersion
            dv = DataVersion.objects.using('default').get(name=key)
            copy = self._data['default'].copy()
            copy.update({
                'NAME': dv.name
            })
            self._data[key] = copy
            return copy
        except Exception as e:
            pass

    def add_db(self, key, name):
        copy = self._data['default'].copy()
        copy.update({
            'NAME': name
        })
        self._data[key] = copy
