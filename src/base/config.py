import yaml
from functools import reduce


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance._data = cls._load_yaml()
        return cls._instance

    @staticmethod
    def _load_yaml():
        # Load the main configuration file
        with open(r'src/base/configuration/app_config.yml', 'r') as file:
            data = yaml.safe_load(file)
        return data

    def get_value(self, *keys):
        try:
            # Access the configuration value using a series of keys
            return reduce(lambda d, key: d[key], keys, self._data)
        except KeyError:
            print(f"Value not found for keys: {keys}")
            return None
