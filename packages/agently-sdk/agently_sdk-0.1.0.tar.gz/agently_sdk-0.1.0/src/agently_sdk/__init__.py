"""
Agently SDK - Official SDK for developing extensions for the Agently framework.

Currently focused on plugin development, with more capabilities planned for future releases.
"""

from agently_sdk._version import __version__

# Import plugin-related components for convenience
from agently_sdk.plugins import Plugin, PluginVariable, agently_function, kernel_function

__all__ = ["Plugin", "PluginVariable", "agently_function", "kernel_function"]
