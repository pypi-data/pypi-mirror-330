"""Validation utilities for JSDC Loader."""

from typing import Any, get_args, get_origin, Union, Type, Dict
from dataclasses import is_dataclass
from enum import Enum
from pydantic import BaseModel
import functools

from .types import _TYPE_HINTS_CACHE

def get_cached_type_hints(cls: Type) -> Dict[str, Any]:
    """Get type hints with caching for performance."""
    if cls not in _TYPE_HINTS_CACHE:
        from typing import get_type_hints
        _TYPE_HINTS_CACHE[cls] = get_type_hints(cls)
    return _TYPE_HINTS_CACHE[cls]

def validate_dataclass(cls: Any) -> None:
    """Validate that the provided class is a dataclass or BaseModel."""
    if not cls:
        raise TypeError("data_class cannot be None")
    if not (is_dataclass(cls) or issubclass(cls, BaseModel)):
        raise TypeError('data_class must be a dataclass or a Pydantic BaseModel')

def validate_type(key: str, value: Any, e_type: Any) -> None:
    """Validate that a value matches the expected type."""
    o_type = get_origin(e_type)
    if o_type is Union:
        if value is not None and not any(isinstance(value, t) for t in get_args(e_type) if t is not type(None)):
            raise TypeError(f'Invalid type for key {key}: expected {e_type}, got {type(value)}')
    elif o_type is not None:
        if not isinstance(value, o_type):
            raise TypeError(f'Invalid type for key {key}: expected {o_type}, got {type(value)}')
    else:
        if not isinstance(value, e_type):
            raise TypeError(f'Invalid type for key {key}: expected {e_type}, got {type(value)}') 