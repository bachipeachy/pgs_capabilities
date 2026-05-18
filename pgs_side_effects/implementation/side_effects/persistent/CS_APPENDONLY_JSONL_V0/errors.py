"""
errors.py — Canonical error types for CS_APPENDONLY_JSONL_V0.

These errors represent contract-level failures, not implementation details.
They are surfaced to CEP via host.py.
"""


class AppendOnlyJsonlError(Exception):
    """Base class for all CS_APPENDONLY_JSONL_V0 errors."""


class InvalidRecord(AppendOnlyJsonlError):
    """Raised when a record fails validation."""


class StorageCorrupt(AppendOnlyJsonlError):
    """Raised when persisted data cannot be read or parsed safely."""


class StorageUnavailable(AppendOnlyJsonlError):
    """Raised when the backend cannot be accessed or written."""
