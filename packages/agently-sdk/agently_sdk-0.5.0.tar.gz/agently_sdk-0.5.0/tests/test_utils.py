"""
Tests for the utility functions.
"""

from agently_sdk.plugins import Plugin, PluginVariable, kernel_function
from agently_sdk.utils.testing import get_plugin_info, validate_plugin


class ValidPlugin(Plugin):
    """A valid plugin for testing."""

    name = "valid_plugin"
    description = "A valid plugin for testing"

    test_var = PluginVariable(name="test_var", description="A test variable", default="default")

    @kernel_function
    def test_function(self) -> str:
        """A test function."""
        return "test"


class InvalidPlugin(Plugin):
    """An invalid plugin for testing."""

    # Missing name
    description = "An invalid plugin for testing"

    # Variable with mismatched name
    test_var = PluginVariable(name="wrong_name", description="A test variable", default="default")

    # No kernel functions


def test_get_plugin_info():
    """Test that get_plugin_info returns the expected information."""
    info = get_plugin_info(ValidPlugin)

    assert info["name"] == "valid_plugin"
    assert info["description"] == "A valid plugin for testing"
    assert "test_var" in info["variables"]
    assert info["variables"]["test_var"]["name"] == "test_var"
    assert info["variables"]["test_var"]["default"] == "default"
    assert "test_function" in info["functions"]


def test_validate_plugin():
    """Test that validate_plugin correctly identifies issues."""
    # Valid plugin should have no issues
    issues = validate_plugin(ValidPlugin)
    assert len(issues) == 0

    # Invalid plugin should have issues
    issues = validate_plugin(InvalidPlugin)
    assert len(issues) > 0

    # Check specific issues
    assert any("missing a name" in issue for issue in issues)
    assert any("mismatched name" in issue for issue in issues)
    assert any("no kernel functions" in issue for issue in issues)
