"""Core functionality for JSDC Loader."""

from .types import T
from .converter import convert_dict_to_dataclass, convert_dataclass_to_dict
from .validator import validate_dataclass, validate_type

__all__ = [
    'T', 
    'convert_dict_to_dataclass', 
    'convert_dataclass_to_dict',
    'validate_dataclass',
    'validate_type',
] 