"""
errors.py — Error definitions for CS_REGISTRY_V0.
"""


class RegistryError(Exception):
    """Base class for registry errors."""


class RegistryKeyExists(RegistryError):
    """Raised when attempting to register an existing key."""


class RegistryKeyNotFound(RegistryError):
    """Raised when a key or address cannot be resolved."""


class StorageUnavailable(RegistryError):
    """Raised when registry storage backend is unavailable."""
