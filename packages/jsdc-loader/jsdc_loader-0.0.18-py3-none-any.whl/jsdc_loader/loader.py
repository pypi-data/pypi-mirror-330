"""Loader functions for deserializing JSON to dataclasses."""

import json
import os
from typing import Union, TextIO, Any

from .core import T, validate_dataclass, convert_dict_to_dataclass
from .file_ops import check_file_size

def jsdc_load(fp: Union[str, TextIO], data_class: T, encoding: str = 'utf-8', max_size: int = 10 * 1024 * 1024) -> T:
    """
    Deserialize a file-like object containing a JSON document to a Python dataclass object.

    :param fp: A .read()-supporting file-like object containing a JSON document
    :param data_class: The dataclass type to deserialize into
    :param encoding: The encoding to use when reading the file (if fp is a string)
    :param max_size: Maximum allowed file size in bytes (default 10MB)
    :return: An instance of the data_class
    :raises: ValueError if file is too large or path is invalid
    :raises: FileNotFoundError if file doesn't exist
    :raises: PermissionError if file can't be accessed 
    :raises: JSONDecodeError if JSON is malformed
    """
    if isinstance(fp, str):
        if not fp or not isinstance(fp, str):
            raise ValueError("Invalid file path")
        
        try:
            check_file_size(fp, max_size)
            
            with open(fp, 'r', encoding=encoding) as f:
                return jsdc_loads(f.read(), data_class)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {fp}")
        except PermissionError:
            raise PermissionError(f"Permission denied accessing file: {fp}")
        except UnicodeDecodeError:
            raise ValueError(f"File encoding error. Expected {encoding} encoding")
    else:
        try:
            content = fp.read()
            if len(content.encode('utf-8')) > max_size:
                raise ValueError(f"Content size exceeds maximum allowed size of {max_size} bytes")
            return jsdc_loads(content, data_class)
        except Exception as e:
            raise ValueError(f"Error reading from file-like object: {str(e)}")

def jsdc_loads(s: str, data_class: T) -> T:
    """
    Deserialize a string containing a JSON document to a Python dataclass object.

    :param s: A string containing a JSON document
    :param data_class: The dataclass type to deserialize into
    :return: An instance of the data_class
    :raises: ValueError if input is invalid or type mismatch occurs
    :raises: TypeError if data_class is not a valid dataclass or BaseModel
    :raises: JSONDecodeError if JSON is malformed
    """
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    
    if not s.strip():
        raise ValueError("Input string is empty or contains only whitespace")

    try:
        data = json.loads(s)
        if not isinstance(data, dict):
            raise ValueError("JSON root must be an object")
        
        validate_dataclass(data_class)
        return convert_dict_to_dataclass(data, data_class)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error during deserialization: {str(e)}") 