"""Dumper functions for serializing dataclasses to JSON."""

import os
from typing import Any
from dataclasses import is_dataclass
from pydantic import BaseModel

from .core import T, convert_dataclass_to_dict
from .file_ops import ensure_directory_exists, save_json_file

def jsdc_dump(obj: T, output_path: str, encoding: str = 'utf-8', indent: int = 4) -> None:
    """Serialize a dataclass or Pydantic BaseModel instance to a JSON file.

    This function takes a dataclass instance and writes its serialized 
    representation to a specified file in JSON format. The output file 
    can be encoded in a specified character encoding, and the JSON 
    output can be formatted with a specified indentation level.

    Args:
        obj (T): The dataclass instance to serialize.
        output_path (str): The path to the output file where the JSON 
                           data will be saved.
        encoding (str, optional): The character encoding to use for the 
                                  output file. Defaults to 'utf-8'.
        indent (int, optional): The number of spaces to use for indentation 
                                in the JSON output. Defaults to 4.

    Raises:
        ValueError: If the provided object is not a dataclass or path is invalid
        TypeError: If obj is not a dataclass or BaseModel
        OSError: If there are file system related errors
        UnicodeEncodeError: If encoding fails
    """
    if not output_path or not isinstance(output_path, str):
        raise ValueError("Invalid output path")
    
    if indent < 0:
        raise ValueError("Indent must be non-negative")

    try:
        # Ensure directory exists and is writable
        directory = os.path.dirname(os.path.abspath(output_path))
        ensure_directory_exists(directory)

        if isinstance(obj, type):
            raise TypeError("obj must be an instance, not a class")
            
        if not (is_dataclass(obj) or isinstance(obj, BaseModel)):
            raise TypeError('obj must be a dataclass or a Pydantic BaseModel instance')
            
        data_dict = convert_dataclass_to_dict(obj)
        save_json_file(output_path, data_dict, encoding, indent)
    except OSError as e:
        raise OSError(f"Failed to create directory or access file: {str(e)}")
    except TypeError as e:
        raise TypeError(f"Type validation failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error during serialization: {str(e)}") 