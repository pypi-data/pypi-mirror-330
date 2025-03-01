"""
Plugin variable system for Agently plugins.
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union


class PluginVariable:
    """
    Represents a configurable variable for a plugin.

    Plugin variables allow plugins to be configured with different values
    when they are loaded by Agently. Variables can have default values,
    validation rules, and type constraints.

    Example:
        ```python
        from agently_sdk.plugins import Plugin, PluginVariable

        class MyPlugin(Plugin):
            name = "my_plugin"
            description = "My awesome plugin"

            # Define a simple string variable with a default value
            greeting = PluginVariable(
                name="greeting",
                description="The greeting to use",
                default_value="Hello"
            )

            # Define a variable with validation
            count = PluginVariable(
                name="count",
                description="Number of times to repeat",
                default_value=1,
                validator=lambda x: isinstance(x, int) and x > 0,
                value_type=int
            )
        ```
    """

    def __init__(
        self,
        name: str,
        description: str,
        default_value: Any = None,
        required: bool = False,
        validator: Optional[Callable[[Any], bool]] = None,
        choices: Optional[List[Any]] = None,
        value_type: Optional[Type] = None,
    ):
        """
        Initialize a plugin variable.

        Args:
            name: The name of the variable.
            description: A description of what the variable is used for.
            default_value: The default value if none is provided.
            required: Whether this variable must be provided.
            validator: Optional function that validates the value.
            choices: Optional list of valid choices for the value.
            value_type: Optional type constraint for the value.
        """
        self.name = name
        self.description = description
        self.default_value = default_value
        self.required = required
        self.validator = validator
        self.choices = choices
        self.value_type = value_type

        # Validate the default value if provided
        if default_value is not None:
            self.validate(default_value)

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

        # Check choices constraint if specified
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
            result["default_value"] = self.default_value

        if self.choices is not None:
            result["choices"] = self.choices

        if self.value_type is not None:
            result["value_type"] = self.value_type.__name__

        return result
