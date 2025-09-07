"""APKPatcher - Android APK manipulation toolkit."""

__version__ = "7.9.2025.1"
__author__ = "APKPatcher Contributors"
__email__ = "contributors@apkpatcher.dev"
__license__ = "MIT"

from .exceptions import APKPatcherError, ToolNotFoundError, ValidationError

__all__ = [
    "APKPatcherError",
    "ToolNotFoundError", 
    "ValidationError"
]
