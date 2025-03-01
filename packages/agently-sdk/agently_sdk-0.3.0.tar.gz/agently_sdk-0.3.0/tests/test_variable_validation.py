"""
Tests for the VariableValidation class.
"""

import re

import pytest

from agently_sdk.plugins.variables import PluginVariable, VariableValidation


def test_variable_validation_options():
    """Test validation with options."""
    validation = VariableValidation(options=["red", "green", "blue"])

    # Valid values
    assert validation.validate("red") == (True, None)
    assert validation.validate("green") == (True, None)
    assert validation.validate("blue") == (True, None)

    # Invalid values
    is_valid, error = validation.validate("yellow")
    assert not is_valid
    assert "must be one of" in error


def test_variable_validation_range():
    """Test validation with range."""
    validation = VariableValidation(range=(1, 10))

    # Valid values
    assert validation.validate(1) == (True, None)
    assert validation.validate(5) == (True, None)
    assert validation.validate(10) == (True, None)

    # Invalid values
    is_valid, error = validation.validate(0)
    assert not is_valid
    assert ">= 1" in error

    is_valid, error = validation.validate(11)
    assert not is_valid
    assert "<= 10" in error


def test_variable_validation_pattern():
    """Test validation with pattern."""
    # Test with string pattern
    validation = VariableValidation(pattern=r"^[a-z]+$")

    # Valid values
    assert validation.validate("abc") == (True, None)
    assert validation.validate("hello") == (True, None)

    # Invalid values
    is_valid, error = validation.validate("123")
    assert not is_valid
    assert "match pattern" in error

    is_valid, error = validation.validate("Hello")
    assert not is_valid
    assert "match pattern" in error

    # Test with compiled pattern
    validation = VariableValidation(pattern=re.compile(r"^[A-Z][a-z]+$"))

    # Valid values
    assert validation.validate("Hello") == (True, None)
    assert validation.validate("World") == (True, None)

    # Invalid values
    is_valid, error = validation.validate("hello")
    assert not is_valid
    assert "match pattern" in error


def test_variable_validation_custom_error():
    """Test validation with custom error message."""
    validation = VariableValidation(
        options=["red", "green", "blue"], error_message="Please choose a valid color"
    )

    # Invalid value with custom error
    is_valid, error = validation.validate("yellow")
    assert not is_valid
    assert error == "Please choose a valid color"


def test_plugin_variable_with_validation():
    """Test PluginVariable with VariableValidation."""
    # Test with options validation
    var = PluginVariable(
        name="color",
        description="Color to use",
        default="blue",
        validation=VariableValidation(options=["red", "green", "blue"]),
    )

    # Valid values
    assert var.validate("red") is True
    assert var.validate("green") is True
    assert var.validate("blue") is True

    # Invalid values
    with pytest.raises(ValueError, match="failed validation"):
        var.validate("yellow")

    # Test with range validation
    var = PluginVariable(
        name="count",
        description="Count value",
        default=5,
        validation=VariableValidation(range=(1, 10)),
    )

    # Valid values
    assert var.validate(1) is True
    assert var.validate(5) is True
    assert var.validate(10) is True

    # Invalid values
    with pytest.raises(ValueError, match="failed validation"):
        var.validate(0)

    with pytest.raises(ValueError, match="failed validation"):
        var.validate(11)

    # Test with pattern validation
    var = PluginVariable(
        name="username",
        description="Username",
        default="user123",
        validation=VariableValidation(pattern=r"^[a-z0-9_]+$"),
    )

    # Valid values
    assert var.validate("user123") is True
    assert var.validate("admin_user") is True

    # Invalid values
    with pytest.raises(ValueError, match="failed validation"):
        var.validate("User123")

    with pytest.raises(ValueError, match="failed validation"):
        var.validate("user@123")


def test_plugin_variable_with_choices():
    """Test that PluginVariable works correctly with choices."""
    # Create a variable with choices
    var = PluginVariable(
        name="color",
        description="Color to use",
        default="blue",
        choices=["red", "green", "blue"],
    )

    # Check that a validation object was created automatically
    assert var.validation is not None
    assert var.validation.options == ["red", "green", "blue"]

    # Valid values
    assert var.validate("red") is True
    assert var.validate("green") is True
    assert var.validate("blue") is True

    # Invalid values
    with pytest.raises(ValueError):
        var.validate("yellow")


def test_to_dict_with_validation():
    """Test that to_dict includes validation information."""
    # Create a variable with validation
    var = PluginVariable(
        name="count",
        description="Count value",
        default=5,
        validation=VariableValidation(
            range=(1, 10), error_message="Count must be between 1 and 10"
        ),
    )

    # Get dictionary representation
    result = var.to_dict()

    # Check validation info
    assert "validation" in result
    assert "range" in result["validation"]
    assert result["validation"]["range"] == (1, 10)
