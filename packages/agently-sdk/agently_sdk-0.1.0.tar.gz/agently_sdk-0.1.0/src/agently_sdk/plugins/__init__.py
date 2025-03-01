"""
Plugin system for Agently - provides base classes and utilities for creating plugins.

This package contains the core components needed to develop plugins for the Agently framework.
"""

from agently_sdk.plugins.base import Plugin
from agently_sdk.plugins.decorators import agently_function, kernel_function
from agently_sdk.plugins.variables import PluginVariable

__all__ = ["Plugin", "PluginVariable", "agently_function", "kernel_function"]
