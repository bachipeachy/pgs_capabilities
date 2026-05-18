"""
errors.py — Canonical error types for CS_SEND_EMAIL_V0.

These errors represent contract-level failures, not implementation details.
They are surfaced to CEP via runtime.py.
"""


class SendEmailError(Exception):
    """Base class for all CS_SEND_EMAIL_V0 errors."""


class InvalidRecipient(SendEmailError):
    """Raised when the recipient email address fails validation."""


class SmtpUnavailable(SendEmailError):
    """Raised when the SMTP backend cannot be reached."""
