"""Deprecated module - will be removed in future versions.

This module is kept for backward compatibility. Please use the new imported functions directly.
"""

import warnings
import functools

from .loader import jsdc_load, jsdc_loads
from .dumper import jsdc_dump

# Display deprecation warning when this module is imported
warnings.warn(
    "The jsdc_loader module is deprecated and will be removed in a future version. "
    "Please import directly from jsdc_loader package instead.",
    DeprecationWarning,
    stacklevel=2
)

# We keep the old exports for backward compatibility
__all__ = ['jsdc_load', 'jsdc_loads', 'jsdc_dump']
