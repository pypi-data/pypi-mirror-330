"""
Plugin variable system for Agently plugins.
"""

# mypy: disable-error-code="assignment"

import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Pattern, Tuple, Type, Union, cast


@dataclass
class VariableValidation:
    """
    Validation rules for plugin variables.

    This class provides a structured way to define validation rules for plugin variables.
    It supports options (choices), range validation, and pattern matching.

    Example:
        ```python
        # Create a validation rule for a string that must match a pattern
        validation = VariableValidation(
            pattern=r"^[a-zA-Z0-9_]+$",
            error_message="Value must contain only alphanumeric characters and underscores"
        )

        # Create a validation rule for a number in a specific range
        validation = VariableValidation(
            range=(0, 100),
            error_message="Value must be between 0 and 100"
        )

        # Create a validation rule with specific options
        validation = VariableValidation(
            options=["red", "green", "blue"],
            error_message="Value must be one of: red, green, blue"
        )
        ```
    """

    options: Optional[List[Any]] = None
    range: Optional[Tuple[Optional[Any], Optional[Any]]] = None
    pattern: Optional[Union[str, Pattern[str]]] = None
    error_message: Optional[str] = None

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a value against the rules.

        Args:
            value: The value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.options is not None and value not in self.options:
            return False, self.error_message or f"Value must be one of: {self.options}"

        if self.range is not None:
            min_val, max_val = self.range
            if min_val is not None and value < min_val:
                return False, self.error_message or f"Value must be >= {min_val}"
            if max_val is not None and value > max_val:
                return False, self.error_message or f"Value must be <= {max_val}"

        if self.pattern is not None:
            if not isinstance(value, str):
                return (
                    False,
                    self.error_message or "Value must be a string for pattern validation",
                )

            # Convert string pattern to compiled pattern if needed
            pattern = self.pattern
            if isinstance(pattern, str):
                pattern = re.compile(pattern)

            if not pattern.match(value):
                return (
                    False,
                    self.error_message or f"Value must match pattern: {self.pattern}",
                )

        return True, None


class PluginVariable:
    """
    Represents a configurable variable for a plugin.

    Plugin variables allow plugins to be configured with different values
    when they are loaded by Agently. Variables can have default values,
    validation rules, and type constraints.

    Example:
        ```python
        from agently_sdk.plugins import Plugin, PluginVariable, VariableValidation

        class MyPlugin(Plugin):
            name = "my_plugin"
            description = "My awesome plugin"

            # Define a simple string variable with a default value
            greeting = PluginVariable(
                name="greeting",
                description="The greeting to use",
                default="Hello"
            )

            # Define a variable with validation
            count = PluginVariable(
                name="count",
                description="Number of times to repeat",
                default=1,
                validation=VariableValidation(range=(1, 10))
            )

            # Define a variable with options
            color = PluginVariable(
                name="color",
                description="Color to use",
                default="blue",
                validation=VariableValidation(options=["red", "green", "blue"])
            )
        ```
    """

    def __init__(
        self,
        description: str,
        default: Any = None,
        type: Optional[Type] = None,
        choices: Optional[List[Any]] = None,
        validator: Optional[Callable[[Any], bool]] = None,
        validation: Optional[VariableValidation] = None,
        sensitive: bool = False,
        # Backward compatibility parameters
        default_value: Optional[Any] = None,
        value_type: Optional[Type] = None,
        name: Optional[str] = None,
    ):
        """
        Initialize a plugin variable.

        Args:
            description: Description of the variable
            default: Default value for the variable
            type: Type of the variable (e.g., str, int, etc.)
            choices: List of valid values for the variable
            validator: Custom validation function
            validation: Validation rules for the variable
            sensitive: Whether the variable contains sensitive information
            default_value: (Deprecated) Use default instead
            value_type: (Deprecated) Use type instead
            name: Name of the variable (optional, will be set from class attribute name)
        """
        self.name = name
        self.description = description

        # Handle backward compatibility
        self.default_value = default if default is not None else default_value
        self.value_type = type if type is not None else value_type

        self.choices = choices
        self.validator = validator
        self.validation = validation
        self.sensitive = sensitive

        # If choices are provided but no validation, create a validation object
        if self.choices is not None and self.validation is None:
            self.validation = VariableValidation(options=self.choices)

        # Validate the default value if provided
        if self.default_value is not None:
            self.validate(self.default_value)

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a value against this variable's constraints.

        Args:
            value: The value to validate

        Returns:
            A tuple of (is_valid, error_message)
        """
        # Check if value is required
        if value is None and self.default_value is None:
            return False, f"Variable '{self.name}' is required but no value was provided"

        # If value is None and there is a default, it's valid
        if value is None:
            return True, None

        # Type validation
        try:
            # Skip type validation if no type is specified
            if self.value_type is not None:
                # Handle nested types like List[str], Dict[str, int], etc.
                if hasattr(self.value_type, "__origin__"):  # For generic types like List, Dict
                    origin = self.value_type.__origin__
                    args = self.value_type.__args__

                    if origin == list:
                        if not isinstance(value, list):
                            return False, f"Variable '{self.name}' must be a list"
                        # Validate each item in the list
                        for item in value:
                            if not isinstance(item, args[0]):
                                return (
                                    False,
                                    f"List items in '{self.name}' must be of type {args[0].__name__}",
                                )

                    elif origin == dict:
                        if not isinstance(value, dict):
                            return False, f"Variable '{self.name}' must be a dictionary"
                        # Validate dict key and value types
                        for k, v in value.items():
                            if not isinstance(k, args[0]):
                                return (
                                    False,
                                    f"Dictionary keys in '{self.name}' must be of type {args[0].__name__}",
                                )
                            if not isinstance(v, args[1]):
                                return (
                                    False,
                                    f"Dictionary values in '{self.name}' must be of type {args[1].__name__}",
                                )
                else:
                    if not isinstance(value, self.value_type):
                        return (
                            False,
                            f"Variable '{self.name}' must be of type {self.value_type.__name__}, got {type(value).__name__}",
                        )
        except Exception as e:
            return False, f"Type validation error for '{self.name}': {str(e)}"

        # Check structured validation if specified
        if self.validation is not None:
            is_valid, error_message = self.validation.validate(value)
            if not is_valid:
                return False, f"Variable '{self.name}' failed validation: {error_message}"

        # Check choices constraint if specified (for backward compatibility)
        if self.choices is not None and value not in self.choices:
            return False, f"Variable '{self.name}' must be one of {self.choices}, got {value}"

        # Check custom validator if specified
        if self.validator is not None:
            try:
                if not self.validator(value):
                    return False, f"Variable '{self.name}' failed custom validation: {value}"
            except Exception as e:
                return False, f"Custom validation error for '{self.name}': {str(e)}"

        return True, None

    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        """
        Descriptor protocol: Get the value of this variable.

        When accessed from an instance, returns the current value.
        When accessed from the class, returns the PluginVariable instance.

        Args:
            obj: The instance the descriptor is accessed from
            objtype: The type of the instance

        Returns:
            Either the current value or self
        """
        if obj is None:
            return self

        # Check if the _values dictionary exists on the instance
        if not hasattr(obj, "_values"):
            obj._values = {}

        # Return the value from the _values dict, or the default if not set
        return obj._values.get(self.name, self.default_value)

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Descriptor protocol: Set the value of this variable.

        Validates the value before setting it.

        Args:
            obj: The instance the descriptor is accessed from
            value: The value to set

        Raises:
            ValueError: If the value is invalid
        """
        # Check if the _values dictionary exists on the instance
        if not hasattr(obj, "_values"):
            obj._values = {}

        # Validate the value
        is_valid, error = self.validate(value)
        if not is_valid:
            raise ValueError(error)

        # Store the value in the _values dictionary
        obj._values[self.name] = value

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this variable to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary with variable metadata.
        """
        result = {
            "name": self.name,
            "description": self.description,
            "sensitive": self.sensitive,
        }

        # Add type if available
        if self.value_type is not None:
            result["type"] = self.value_type.__name__

        # Add default value if available
        if self.default_value is not None:
            result["default"] = self.default_value

        # Add choices if available
        if self.choices is not None:
            result["choices"] = self.choices

        # Add validation info if available
        if self.validation is not None:
            validation_info: Dict[str, Any] = {}

            if self.validation.options is not None:
                validation_info["options"] = self.validation.options  # type: ignore[assignment]

            if self.validation.range is not None:
                validation_info["range"] = self.validation.range  # type: ignore

            if self.validation.pattern is not None:
                if hasattr(self.validation.pattern, "pattern"):
                    validation_info["pattern"] = self.validation.pattern.pattern  # type: ignore
                else:
                    validation_info["pattern"] = str(self.validation.pattern)

            if self.validation.error_message is not None:
                validation_info["error_message"] = self.validation.error_message

            if validation_info:
                result["validation"] = validation_info  # type: ignore

        return result


__all__ = ["PluginVariable", "VariableValidation"]
