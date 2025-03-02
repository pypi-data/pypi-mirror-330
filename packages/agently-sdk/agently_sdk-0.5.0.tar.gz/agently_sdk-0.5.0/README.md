# Agently SDK

[![PyPI version](https://badge.fury.io/py/agently-sdk.svg)](https://badge.fury.io/py/agently-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The official SDK for developing extensions for the [Agently](https://github.com/onwardplatforms/agently) framework. Currently focused on plugin development, with more capabilities planned for future releases.

## Installation

```bash
pip install agently-sdk
```

## Quick Start

Create a simple plugin:

```python
from agently_sdk.plugins import Plugin, PluginVariable, kernel_function

class HelloPlugin(Plugin):
    name = "hello"
    description = "A simple hello world plugin"
    
    default_name = PluginVariable(
        name="default_name",
        description="Default name to use in greetings",
        default="World"
    )
    
    @kernel_function
    def greet(self, name=None) -> str:
        """Greet the user."""
        return f"Hello, {name or self.default_name}!"
```

## Plugin Development

### Plugin Class

The `Plugin` class is the base class for all Agently plugins. It provides the structure and interface for creating plugins that can be used by Agently agents.

| Attribute     | Type  | Required | Description                                     |
| ------------- | ----- | -------- | ----------------------------------------------- |
| `name`        | `str` | Yes      | The name of the plugin, used for identification |
| `description` | `str` | Yes      | A brief description of what the plugin does     |

#### Methods

| Method                   | Description                                                                 |
| ------------------------ | --------------------------------------------------------------------------- |
| `get_kernel_functions()` | Returns a dictionary of all methods decorated with `@kernel_function`       |
| `get_plugin_variables()` | Returns a dictionary of all `PluginVariable` instances defined in the class |

### PluginVariable

The `PluginVariable` class represents a configurable variable for a plugin. It allows plugins to be configured with different values when they are loaded by Agently.

| Parameter     | Type                    | Required | Default | Description                                    |
| ------------- | ----------------------- | -------- | ------- | ---------------------------------------------- |
| `name`        | `str`                   | Yes      | -       | The name of the variable                       |
| `description` | `str`                   | Yes      | -       | A description of what the variable is used for |
| `default`     | `Any`                   | No       | `None`  | The default value if none is provided          |
| `required`    | `bool`                  | No       | `False` | Whether this variable must be provided         |
| `validator`   | `Callable[[Any], bool]` | No       | `None`  | Optional function that validates the value     |
| `choices`     | `List[Any]`             | No       | `None`  | Optional list of valid choices for the value   |
| `type`        | `Type`                  | No       | `None`  | Optional type constraint for the value         |

#### Methods

| Method            | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `validate(value)` | Validates a value against this variable's constraints |
| `to_dict()`       | Converts this variable to a dictionary representation |

### Kernel Function Decorator

Agently SDK provides two decorators for marking methods as callable by agents:

1. `@agently_function` - The recommended decorator for Agently plugins
2. `@kernel_function` - An alias for `@agently_function` provided for backward compatibility

Both decorators wrap the `kernel_function` decorator from `semantic_kernel.functions` while maintaining compatibility with our existing code. If the Semantic Kernel package is not available, they fall back to a compatible implementation.

```python
from agently_sdk.plugins import Plugin, PluginVariable, agently_function

class MyPlugin(Plugin):
    name = "my_plugin"
    description = "A sample plugin"
    
    @agently_function
    def my_function(self, param1: str, param2: int = 0) -> str:
        """
        Function docstring that describes what this function does.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Description of the return value
        """
        # Implementation
        return result
```

## Best Practices

### Plugin Design

1. **Clear Purpose**: Each plugin should have a clear, focused purpose
2. **Descriptive Names**: Use descriptive names for plugins, variables, and functions
3. **Comprehensive Documentation**: Include detailed docstrings for all functions
4. **Input Validation**: Validate all inputs to ensure robust behavior
5. **Error Handling**: Handle errors gracefully and provide informative error messages

### Variable Configuration

1. **Default Values**: Provide sensible default values for variables when possible
2. **Validation**: Use validators to ensure variables meet requirements
3. **Type Constraints**: Specify value types to catch type errors early
4. **Descriptive Names**: Use clear, descriptive names for variables

## License

MIT 