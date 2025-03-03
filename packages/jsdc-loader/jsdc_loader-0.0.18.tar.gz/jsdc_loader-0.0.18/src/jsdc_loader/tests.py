"""Test cases for JSDC Loader."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict
import tempfile
import os
import unittest

from pydantic import BaseModel

from .loader import jsdc_load, jsdc_loads
from .dumper import jsdc_dump

class TestJSDCLoader(unittest.TestCase):
    """Test suite for JSDC Loader."""
    
    def setUp(self):
        """Set up the test environment."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        
    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
    
    def test_basic_serialization(self):
        """Test basic dataclass serialization/deserialization."""
        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
            user: str = 'root'
            password: str = 'password'
            ips: List[str] = field(default_factory=lambda: ['127.0.0.1'])
            primary_user: Optional[str] = field(default_factory=lambda: None)
        
        db = DatabaseConfig()
        jsdc_dump(db, self.temp_path)
        loaded_db = jsdc_load(self.temp_path, DatabaseConfig)
        
        self.assertEqual(db.host, loaded_db.host)
        self.assertEqual(db.port, loaded_db.port)
        self.assertEqual(db.ips, loaded_db.ips)
    
    def test_enum_serialization(self):
        """Test enum serialization/deserialization."""
        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass 
        class UserConfig:
            name: str = 'John Doe'
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ['read'])
        
        user = UserConfig()
        jsdc_dump(user, self.temp_path)
        loaded_user = jsdc_load(self.temp_path, UserConfig)
        
        self.assertEqual(user.name, loaded_user.name)
        self.assertEqual(user.user_type, loaded_user.user_type)
    
    def test_nested_dataclasses(self):
        """Test nested dataclasses serialization/deserialization."""
        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass 
        class UserConfig:
            name: str = 'John Doe'
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ['read'])

        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
            user: str = 'root'
            password: str = 'password'
            ips: List[str] = field(default_factory=lambda: ['127.0.0.1'])
            primary_user: Optional[str] = field(default_factory=lambda: None)

        @dataclass
        class AppConfig:
            user: UserConfig = field(default_factory=lambda: UserConfig())
            database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
            version: str = '1.0.0'
            debug: bool = False
            settings: Dict[str, str] = field(default_factory=lambda: {'theme': 'dark'})
        
        app = AppConfig()
        app.user.roles.append('write')
        app.database.ips.extend(['192.168.1.1', '10.0.0.1'])
        app.settings['language'] = 'en'
        
        jsdc_dump(app, self.temp_path)
        loaded_app = jsdc_load(self.temp_path, AppConfig)
        
        self.assertEqual(loaded_app.user.roles, ['read', 'write'])
        self.assertEqual(loaded_app.database.ips, ['127.0.0.1', '192.168.1.1', '10.0.0.1'])
        self.assertEqual(loaded_app.settings, {'theme': 'dark', 'language': 'en'})
    
    def test_pydantic_models(self):
        """Test Pydantic models serialization/deserialization."""
        class ServerConfig(BaseModel):
            name: str = "main"
            port: int = 8080
            ssl: bool = True
            headers: Dict[str, str] = {"Content-Type": "application/json"}

        class ApiConfig(BaseModel):
            servers: List[ServerConfig] = []
            timeout: int = 30
            retries: int = 3
        
        api_config = ApiConfig()
        api_config.servers.append(ServerConfig(name="backup", port=8081))
        api_config.servers.append(ServerConfig(name="dev", port=8082, ssl=False))
        
        jsdc_dump(api_config, self.temp_path)
        loaded_api = jsdc_load(self.temp_path, ApiConfig)
        
        self.assertEqual(len(loaded_api.servers), 2)
        self.assertEqual(loaded_api.servers[0].name, "backup")
        self.assertEqual(loaded_api.servers[1].port, 8082)
        self.assertFalse(loaded_api.servers[1].ssl)
    
    def test_error_handling(self):
        """Test error handling."""
        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
        
        # Test nonexistent file
        with self.assertRaises(FileNotFoundError):
            jsdc_load("nonexistent.json", DatabaseConfig)
        
        # Test empty input
        with self.assertRaises(ValueError):
            jsdc_loads("", DatabaseConfig)
        
        # Test invalid JSON
        with self.assertRaises(ValueError):
            jsdc_loads("{invalid json}", DatabaseConfig)
        
        # Test invalid indent
        with self.assertRaises(ValueError):
            jsdc_dump(DatabaseConfig(), self.temp_path, indent=-1)

if __name__ == '__main__':
    unittest.main() 