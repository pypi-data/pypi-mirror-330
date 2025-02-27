import sys
import builtins
from rich.text import Text
from rich.console import Console
from abc import ABCMeta
from typing import Any, Dict, List, Optional, Union, Callable

# Configuration class to replace global variables
class Config:
    """Configuration manager for custom representation settings."""
    def __init__(self):
        self.show_attributes = True  
        self.show_methods = True
        self._original_build_class = builtins.__build_class__
    
    def update(self, show_attributes: Optional[bool] = None, show_methods: Optional[bool] = None) -> None:
        """
        Update configuration settings.
        
        Args:
            show_attributes: Whether to display object attributes
            show_methods: Whether to display object methods
        """
        if show_attributes is not None:
            self.show_attributes = show_attributes
        if show_methods is not None:
            self.show_methods = show_methods
    
    @property
    def original_build_class(self) -> Callable:
        """Return the original __build_class__ function."""
        return self._original_build_class


# Create a singleton configuration object
config = Config()


def custom_repr_config(attributes: bool = True, methods: bool = True) -> None:
    """
    Configure the output format of custom_repr.
    
    Args:
        attributes: Whether to show attributes (default: True)
        methods: Whether to show methods (default: True)
    
    Examples:
        >>> custom_repr_config(True, False)  # Show attributes only
        >>> custom_repr_config(False, True)  # Show methods only
        >>> custom_repr_config(True, True)   # Show both attributes and methods
        >>> custom_repr_config(False, False) # Show class name only
    """
    config.update(show_attributes=attributes, show_methods=methods)


def _format_value(value: Any) -> Text:
    """
    Format a value with appropriate styling based on its type.
    
    Args:
        value: The value to format
        
    Returns:
        A rich Text object with appropriate styling
    """
    if isinstance(value, str):
        return Text(f'"{value}"', style="green")  # strings in green
    elif isinstance(value, bool):
        return Text(str(value), style="cyan")  # booleans in cyan
    elif isinstance(value, (int, float)):
        return Text(str(value), style="magenta")  # numbers in magenta
    else:
        return Text(repr(value), style="white")  # other values in white


def custom_repr(self) -> str:
    """
    Custom representation for enhanced object display.
    
    This function provides a rich, colorized string representation of objects,
    displaying their attributes and methods based on current configuration.
    
    Returns:
        A formatted string representation of the object
    """
    console = Console()
    
    # Get attributes with colors
    attribute_list = []
    if config.show_attributes:
        for key, value in self.__dict__.items():
            key_text = Text(key, style="yellow")  # keys in yellow
            colon_text = Text(": ", style="white")
            formatted_value = _format_value(value)
            
            attribute_string = Text.assemble(key_text, colon_text, formatted_value)
            attribute_list.append(attribute_string)
    
    # Get methods
    method_list = []
    if config.show_methods:
        for key, value in type(self).__dict__.items():
            if callable(value) and not key.startswith('__'):
                method_text = Text(f"{key}()", style="magenta")  # methods in magenta
                method_list.append(method_text)
    
    # Create output with colors
    class_name = Text(self.__class__.__name__, style="bold blue")
    
    # If both attributes and methods are disabled, only display the class name
    if not config.show_attributes and not config.show_methods:
        with console.capture() as capture:
            console.print(class_name)
        return capture.get().rstrip()
    
    # Build the full output
    output = Text()
    output.append(class_name)
    output.append(Text(" => ", style="white"))
    
    if config.show_attributes:
        output.append("{ ")
        if attribute_list:
            output.append(Text.join(Text(", "), attribute_list))
        output.append(" }")
    
    # Append methods if there are any and they should be shown
    if config.show_methods and method_list:
        output.append(" || [ ")
        output.append(Text.join(Text(", "), method_list))
        output.append(" ]")
    
    # Capture and return the colored output
    with console.capture() as capture:
        console.print(output)
    return capture.get().rstrip()


class CustomMeta(ABCMeta):
    """
    Custom metaclass that adds enhanced string representation to classes.
    
    This metaclass automatically adds the custom_repr method to all classes
    that use it, unless they already define their own __repr__ method.
    """
    def __new__(cls, name, bases, dct):
        # Only add __repr__ if the class doesn't already define one
        if '__repr__' not in dct:
            dct['__repr__'] = custom_repr
        return super().__new__(cls, name, bases, dct)


def is_user_module(module_name: str, module_file: Optional[str]) -> bool:
    """
    Check if a module is a user-created module.
    
    Args:
        module_name: The name of the module
        module_file: The file path of the module
        
    Returns:
        True if the module is user-created, False otherwise
    """
    if not module_file:  # Built-in modules don't have a file
        return False
        
    # Get the virtual environment path if it exists
    venv_path = sys.prefix

    # Check if the module is from standard library or site-packages
    is_stdlib = module_file.startswith(sys.prefix) or module_file.startswith(sys.base_prefix)
    is_site_packages = 'site-packages' in module_file or 'dist-packages' in module_file
    
    return not (is_stdlib or is_site_packages)


def custom_build_class(func, name, *args, **kwargs):
    """
    Custom implementation of __build_class__ that applies the CustomMeta metaclass.
    
    This function intercepts class definitions and applies the CustomMeta metaclass
    to user-defined classes, adding enhanced string representation.
    
    Args:
        func: The function defining the class body
        name: The name of the class
        *args: Base classes
        **kwargs: Additional keyword arguments
        
    Returns:
        The constructed class
    """
    # Check if the class inherits from ABC but doesn't have a metaclass specified
    is_abc_class = any(arg.__name__ == 'ABC' for arg in args if hasattr(arg, '__name__'))
    
    # Check for metaclass in kwargs
    has_metaclass = 'metaclass' in kwargs
    
    # Check if metaclass is directly ABCMeta
    is_abcmeta_metaclass = False
    if has_metaclass:
        metaclass = kwargs['metaclass']
        is_abcmeta_metaclass = hasattr(metaclass, '__name__') and metaclass.__name__ == 'ABCMeta'
    
    # If it inherits from ABC or uses ABCMeta directly, use CustomMeta
    if (is_abc_class or is_abcmeta_metaclass) and not (has_metaclass and not is_abcmeta_metaclass):
        kwargs['metaclass'] = CustomMeta
    # For normal classes with no metaclass specified
    elif not has_metaclass and not any(isinstance(base, type) and type(base) is not type for base in args):
        kwargs['metaclass'] = CustomMeta
    
    # Call the original build class function with our updated kwargs
    try:
        return config.original_build_class(func, name, *args, **kwargs)
    except Exception as e:
        # Fall back to original implementation if our custom approach fails
        print(f"Warning: custom_repr encountered an error: {e}. Falling back to default behavior.")
        return config.original_build_class(func, name, *args, **kwargs)

# Apply the monkey-patch only when explicitly requested or when module is imported
def apply_patch():
    """Apply the custom __build_class__ patch to Python's builtins."""
    builtins.__build_class__ = custom_build_class

def remove_patch():
    """Remove the custom __build_class__ patch, restoring the original implementation."""
    builtins.__build_class__ = config.original_build_class

# Apply the patch by default
apply_patch()