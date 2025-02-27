"""
Custom Repr - Enhanced Object Representation for Python

This package provides enhanced, colorful representation of Python objects
in interactive sessions and debugging. It automatically adds rich, structured
output for all your classes without modifying their code.

Usage:
    import custom_repr  # This automatically applies the enhancement

    # Configure what to show
    from custom_repr import custom_repr_config
    custom_repr_config(attributes=True, methods=False)  # Show only attributes
"""

from .core import (
    custom_repr,
    custom_repr_config, 
    CustomMeta, 
    apply_patch, 
    remove_patch
)

# Apply the patch when the package is imported
apply_patch()

# Export public API
__all__ = [
    'custom_repr', 
    'custom_repr_config', 
    'CustomMeta', 
    'apply_patch', 
    'remove_patch'
]

__version__ = "2.3.0"