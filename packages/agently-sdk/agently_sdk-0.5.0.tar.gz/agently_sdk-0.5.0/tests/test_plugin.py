"""
Tests for the Plugin base class.
"""

import pytest

from agently_sdk.plugins import Plugin, PluginVariable, kernel_function


class SamplePlugin(Plugin):
    """Sample plugin for unit tests."""

    name = "sample_plugin"
    description = "A plugin for testing"

    test_var = PluginVariable(name="test_var", description="A test variable", default="default")

    number_var = PluginVariable(
        name="number_var", description="A numeric variable", default=42, type=int
    )

    @kernel_function
    def test_function(self, input_str: str) -> str:
        """Test function that returns the input string."""
        return input_str

    @kernel_function
    def use_var(self) -> str:
        """Test function that uses a plugin variable."""
        return self.test_var

    def not_kernel_function(self) -> str:
        """This is not a kernel function."""
        return "not a kernel function"


def test_plugin_initialization():
    """Test that a plugin can be initialized with variables."""
    plugin = SamplePlugin(test_var="custom value")
    assert plugin.test_var == "custom value"
    assert plugin.number_var == 42  # Default value


def test_get_kernel_functions():
    """Test that get_kernel_functions returns only kernel functions."""
    functions = SamplePlugin.get_kernel_functions()

    assert "test_function" in functions
    assert "use_var" in functions
    assert "not_kernel_function" not in functions
    assert len(functions) == 2


def test_plugin_variable_validation():
    """Test that plugin variables validate values."""
    # Should work fine
    plugin = SamplePlugin(number_var=100)
    assert plugin.number_var == 100

    # Should raise ValueError due to wrong type
    with pytest.raises(ValueError):
        SamplePlugin(number_var="not a number")


def test_kernel_function_execution():
    """Test that kernel functions can be executed."""
    plugin = SamplePlugin()
    result = plugin.test_function("hello")
    assert result == "hello"

    result = plugin.use_var()
    assert result == "default"
