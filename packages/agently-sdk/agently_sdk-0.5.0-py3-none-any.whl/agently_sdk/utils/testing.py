"""
Utilities for testing Agently plugins.

This module provides functions for inspecting and validating plugins.
"""

from typing import Any, Dict, List, Optional, Type

from agently_sdk.plugins import Plugin


def get_plugin_info(plugin_class: Type[Plugin]) -> Dict[str, Any]:
    """
    Get information about a plugin class.

    Args:
        plugin_class: The plugin class to inspect.

    Returns:
        Dict[str, Any]: A dictionary containing plugin metadata.
    """
    variables = plugin_class.get_plugin_variables()
    variable_info = {name: var.to_dict() for name, var in variables.items()}

    # Get kernel functions directly from the class
    functions = plugin_class.get_kernel_functions()
    function_names = list(functions.keys())

    return {
        "name": plugin_class.name,
        "description": plugin_class.description,
        "variables": variable_info,
        "functions": function_names,
    }


def validate_plugin(plugin_class: Type[Plugin]) -> List[str]:
    """
    Validate a plugin class and return any issues found.

    Args:
        plugin_class: The plugin class to validate.

    Returns:
        List[str]: A list of validation issues, empty if no issues found.
    """
    issues = []

    # Check for required attributes
    if not hasattr(plugin_class, "name") or not plugin_class.name:
        issues.append("Plugin is missing a name attribute")

    if not hasattr(plugin_class, "description") or not plugin_class.description:
        issues.append("Plugin is missing a description attribute")

    # Check that there's at least one kernel function
    functions = plugin_class.get_kernel_functions()
    if not functions:
        issues.append("Plugin has no kernel functions")

    # Check plugin variables
    variables = plugin_class.get_plugin_variables()
    for name, var in variables.items():
        # Check that the variable name matches the attribute name
        if var.name != name:
            issues.append(f"Variable '{name}' has mismatched name attribute '{var.name}'")

    return issues
