

class DynamicDbDict(dict):
    """
    This dictionary allows to dinamically create connections for databases even when Django is already running.
    This is intended to be use as a settings.DATABASES replacement. Check README.MD for more details.
    When a database is not available directly on the dictionary, the dict will search in the data versions table and
    create a database config dictionary on the fly, to trick Django into thinking that the database existed from the
    very beginning of the execution.
    """
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
