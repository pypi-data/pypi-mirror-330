"""JSDC Loader - JSON to DataClass converter.

This package provides utilities for converting between JSON and Python dataclasses.
It handles nested dataclasses, enums, and Pydantic models.
"""

from .loader import jsdc_load, jsdc_loads
from .dumper import jsdc_dump

__all__ = ['jsdc_load', 'jsdc_loads', 'jsdc_dump']

__version__ = '0.2.0'