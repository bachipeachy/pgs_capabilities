"""
errors.py — Canonical error types for CS_MUTABLE_JSON_V0.

These errors represent contract-level failures, not implementation details.
They are surfaced to CEP via host.py.
"""


class MutableJsonError(Exception):
    """Base class for all CS_MUTABLE_JSON_V0 errors."""


class InvalidKey(MutableJsonError):
    """Raised when a key fails validation (type, format, emptiness)."""


class KeyNotFound(MutableJsonError):
    """Raised when a requested key does not exist."""


class StorageCorrupt(MutableJsonError):
    """Raised when persisted data cannot be read or parsed safely."""


class StorageUnavailable(MutableJsonError):
    """Raised when the backend cannot be accessed or written."""
