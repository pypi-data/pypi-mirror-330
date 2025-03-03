"""Type definitions for JSDC Loader."""

from typing import TypeVar, Union, Dict, Type, Any
from dataclasses import dataclass
from pydantic import BaseModel

# Cache for type hints to avoid repeated lookups
_TYPE_HINTS_CACHE: Dict[Type, Dict[str, Any]] = {}

# Type alias for dataclass or BaseModel
T = TypeVar('T', bound=Union[dataclass, BaseModel]) 