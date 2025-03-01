"""
Plugin variable system for Agently plugins.
"""

import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Pattern, Tuple, Type, Union


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
    pattern: Optional[Union[str, Pattern]] = None
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
        name: str,
        description: str,
        default: Any = None,
        required: bool = False,
        validator: Optional[Callable[[Any], bool]] = None,
        choices: Optional[List[Any]] = None,
        type: Optional[Type] = None,
        validation: Optional[VariableValidation] = None,
    ):
        """
        Initialize a plugin variable.

        Args:
            name: The name of the variable.
            description: A description of what the variable is used for.
            default: The default value if none is provided.
            required: Whether this variable must be provided.
            validator: Optional function that validates the value.
            choices: Optional list of valid choices for the value.
            type: Optional type constraint for the value.
            validation: Optional structured validation rules.
        """
        self.name = name
        self.description = description
        self.default_value = default
        self.required = required
        self.validator = validator
        self.choices = choices
        self.value_type = type
        self.validation = validation

        # For backward compatibility, if choices are provided but no validation,
        # create a validation object with those choices
        if self.validation is None and self.choices is not None:
            self.validation = VariableValidation(options=self.choices)

        # Validate the default value if provided
        if self.default_value is not None:
            self.validate(self.default_value)

    def validate(self, value: Any) -> bool:
        """
        Validate a value against this variable's constraints.

        Args:
            value: The value to validate.

        Returns:
            bool: True if the value is valid.

        Raises:
            ValueError: If the value is invalid.
        """
        # Check if value is required but None
        if self.required and value is None:
            raise ValueError(f"Variable '{self.name}' is required but no value was provided")

        # If value is None and not required, it's valid
        if value is None and not self.required:
            return True

        # Check type constraint if specified
        if self.value_type is not None and not isinstance(value, self.value_type):
            raise ValueError(
                f"Variable '{self.name}' must be of type {self.value_type.__name__}, "
                f"got {type(value).__name__}"
            )

        # Check structured validation if specified
        if self.validation is not None:
            is_valid, error_message = self.validation.validate(value)
            if not is_valid:
                raise ValueError(f"Variable '{self.name}' failed validation: {error_message}")

        # Check choices constraint if specified (for backward compatibility)
        if self.choices is not None and value not in self.choices:
            raise ValueError(f"Variable '{self.name}' must be one of {self.choices}, got {value}")

        # Check custom validator if specified
        if self.validator is not None and not self.validator(value):
            raise ValueError(f"Variable '{self.name}' failed validation: {value}")

        return True

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

        # Use a private attribute on the instance to store the value
        # This ensures each instance has its own value
        private_name = f"_{self.name}_value"
        if not hasattr(obj, private_name):
            setattr(obj, private_name, self.default_value)

        return getattr(obj, private_name)

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Descriptor protocol: Set the value of this variable.

        Validates the value before setting it.

        Args:
            obj: The instance the descriptor is accessed from
            value: The value to set
        """
        if self.validate(value):
            # Store the value in a private attribute on the instance
            private_name = f"_{self.name}_value"
            setattr(obj, private_name, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this variable to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary with variable metadata.
        """
        result = {
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }

        if self.default_value is not None:
            result["default"] = self.default_value

        if self.choices is not None:
            result["choices"] = self.choices

        if self.value_type is not None:
            result["type"] = self.value_type.__name__

        if self.validation is not None:
            validation_info: Dict[str, Any] = {}
            if self.validation.options is not None:
                validation_info["options"] = self.validation.options
            if self.validation.range is not None:
                validation_info["range"] = self.validation.range  # type: ignore
            if self.validation.pattern is not None:
                pattern = self.validation.pattern
                if hasattr(pattern, "pattern"):
                    validation_info["pattern"] = pattern.pattern  # type: ignore
                else:
                    validation_info["pattern"] = str(pattern)
            result["validation"] = validation_info

        return result


__all__ = ["PluginVariable", "VariableValidation"]
