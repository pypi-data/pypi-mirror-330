# JSDC Loader (JSON Data Class Loader)

JSDC Loader is a Python utility for loading JSON configuration files into dataclass objects. It provides a simple and type-safe way to manage configuration data in your Python applications by forcing the use of dataclass and type hinting.

## Features

- Load JSON configuration files into dataclass objects
- Support for nested dataclass structures
- Type checking and conversion for configuration values
- Easy updating of configuration from different files
- Ability to dump modified configurations back to JSON

## Installation

To install JSDC Loader, you can use pip:
```bash
pip install jsdc_loader
```

## Usage

Here's an example of how to use JSDC Loader:

### Example 1
```python
from dataclasses import dataclass
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class DatabaseConfig:
    host: str = 'localhost'  # default value must be provided
    port: int = 3306
    user: str = 'root'
    password: str = 'password'

# Dump configuration to 'config.json'
db_config = DatabaseConfig()
jsdc_dump(db_config, 'config.json')

# Load configuration from 'config.json'
loaded_db_config = jsdc_load('config.json', DatabaseConfig)
print(loaded_db_config.host)  # Accessing the host attribute from the loaded data
```

### Example 2
```python
from dataclasses import dataclass, field
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class UserConfig:
    name: str = 'John Doe'
    age: int = 30

@dataclass
class AppConfig:
    user: UserConfig = field(default_factory=lambda: UserConfig())
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())

# Dump configuration to 'config.json'
app_config = AppConfig()
jsdc_dump(app_config, 'config.json')

# Load configuration from 'config.json'
loaded_app_config = jsdc_load('config.json', AppConfig)
print(loaded_app_config.user.name)  # Accessing the name attribute from the loaded data
```

### Example 3
```python
from dataclasses import dataclass, field
from enum import Enum, auto
from jsdc_loader import jsdc_load, jsdc_dump

class UserType(Enum):
    ADMIN = auto()
    USER = auto()

@dataclass
class UserConfig:
    name: str = 'John Doe'
    age: int = 30
    married: bool = False
    user_type: UserType = field(default_factory=lambda: UserType.USER)

@dataclass
class AppConfig:
    user: UserConfig = field(default_factory=lambda: UserConfig())
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())

# Dump configuration to 'config.json'
app_config = AppConfig()
jsdc_dump(app_config, 'config.json')

# Load configuration from 'config.json'
loaded_app_config = jsdc_load('config.json', AppConfig)
print(loaded_app_config.user.user_type)  # Accessing the user type attribute from the loaded data
```

### Example 4
```python
from dataclasses import dataclass, field
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class ControllerConfig:
    controller_id: str = 'controller_01'
    controller_type: str = 'controller_type_01'
    controller_version: str = 'controller_version_01'
    utc_offset: float = 0.0
    app: AppConfig = field(default_factory=lambda: AppConfig())

# Dump configuration to 'config.json'
controller_config = ControllerConfig()
jsdc_dump(controller_config, 'config.json')

# Load configuration from 'config.json'
loaded_controller_config = jsdc_load('config.json', ControllerConfig)
print(loaded_controller_config.controller_id)  # Accessing the controller_id attribute from the loaded data
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
