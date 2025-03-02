# simpleConfigManager

`simpleConfigManager` is a simple Python library for managing application configuration using JSON files and environment variables.

## Installation

```bash
pip install simpleConfigManager
```

## Usage

```python
from simpleConfigManager import load_config

config_json = {
    "host": {
        "env": "APPLICATION_HOST",
        "default": "localhost",
        "datatype": "STRING",
        "required": True
    },
    "port": {
        "env": "APPLICATION_PORT",
        "default": 3200,
        "datatype": "INT",
        "required": True
    }
}

config = load_config(config_json)
print(config)
```

## Configuration Structure

The configuration JSON structure is as follows:

```json
{
    "key": {
        "env": "ENV_VARIABLE_NAME",
        "default": "default_value",
        "datatype": "STRING",
        "required": true
    }
}
```

## Datatype Support

The library supports the following datatypes:

- STRING
- INT
- FLOAT
- BOOLEAN
- LIST

## Validation

The library will validate the configuration based on the datatype and required fields.

## Example

```python
from simpleConfigManager import load_config

config_json = {
    "host": {
        "env": "APPLICATION_HOST",
        "default": "localhost",
        "datatype": "STRING",
        "required": True
    },
    "port": {
        "env": "APPLICATION_PORT",
        "default": 3200,
        "datatype": "INT",
        "required": True
    }
}

config = load_config(config_json)
print(config)
```

## Testing

```bash
python -m unittest tests/test_config_loader.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

For any questions or feedback, please contact me at [bharadwajadapala28@gmail.com](mailto:bharadwajadapala28@gmail.com).
