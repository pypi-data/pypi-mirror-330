"""File operations for JSDC Loader."""

import os
import json
from typing import Dict, Any

def ensure_directory_exists(directory_path: str) -> None:
    """Ensure the directory exists and is writable."""
    if directory_path:
        if os.path.exists(directory_path):
            if not os.access(directory_path, os.W_OK):
                raise OSError(f"No write permission for directory: {directory_path}")
        else:
            try:
                os.makedirs(directory_path)
            except OSError as e:
                raise OSError(f"Failed to create directory {directory_path}: {str(e)}")

def save_json_file(file_path: str, data: Dict[str, Any], encoding: str, indent: int) -> None:
    """Save a dictionary to a JSON file."""
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(obj=data, fp=f, indent=indent)
    except OSError as e:
        raise OSError(f"Failed to write to file {file_path}: {str(e)}")
    except UnicodeEncodeError as e:
        raise UnicodeEncodeError(f"Failed to encode data with {encoding}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error during JSON serialization: {str(e)}")

def check_file_size(file_path: str, max_size: int) -> int:
    """Check if file size is within limits."""
    file_size = os.path.getsize(file_path)
    if file_size > max_size:
        raise ValueError(f"File size {file_size} bytes exceeds maximum allowed size of {max_size} bytes")
    return file_size 