import os
import json

class ConfigLoader:
    def __init__(self, config_json):
        self.config_json = config_json
        self.config = {}

    def load(self):
        self.config = self._load_config(self.config_json)
        return self.config

    def _load_config(self, config, parent_key=''):
        loaded_config = {}
        for key, value in config.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict) and 'env' not in value:
                loaded_config[key] = self._load_config(value, full_key)
            else:
                loaded_config[key] = self._get_value(value)
        return loaded_config

    def _get_value(self, config_item):
        env_value = os.getenv(config_item['env'])
        if env_value is not None:
            return self._cast_value(env_value, config_item['datatype'])
        return config_item['default']

    def _cast_value(self, value, datatype):
        if datatype == 'INT':
            return int(value)
        elif datatype == 'BOOLEAN':
            return value.lower() in ('true', '1', 'yes')
        elif datatype == 'LIST':
            return value.split(',')
        return value

def load_config(config_json):
    loader = ConfigLoader(config_json)
    return loader.load()