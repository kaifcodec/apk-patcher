"""Custom exceptions for APKPatcher."""


class APKPatcherError(Exception):
    """Base exception for APKPatcher."""
    pass


class ToolNotFoundError(APKPatcherError):
    """Raised when a required tool is not found."""
    pass


class ValidationError(APKPatcherError):
    """Raised when input validation fails.""" 
    pass


class BuildError(APKPatcherError):
    """Raised when APK build operation fails."""
    pass


class SigningError(APKPatcherError):
    """Raised when APK signing fails."""
    pass


class ADBError(APKPatcherError):
    """Raised when ADB operation fails."""
    pass


class FridaPatchError(APKPatcherError):
    """Raised when Frida patching fails."""
    pass


class NetworkError(APKPatcherError):
    """Raised when network operation fails."""
    pass
