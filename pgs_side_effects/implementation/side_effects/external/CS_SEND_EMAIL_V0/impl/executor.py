"""
executor.py — Capability semantics for CS_SEND_EMAIL_V0.

SMTP-based email sending with testbed-safe skipping.
If SMTP environment variables are not configured, returns SUCCESS
with delivery_status: "skipped" instead of failing.
"""

import os
import smtplib
from email.mime.text import MIMEText
from typing import Any, Dict

from pgs_side_effects.implementation.side_effects.external.CS_SEND_EMAIL_V0.errors import (
    InvalidRecipient,
    SmtpUnavailable,
)


TEMPLATES = {
    "wallet_created_notification": (
        "Your wallet {wallet_id} ({wallet_type}) has been created successfully."
    ),
}


class SendEmailEngine:
    """SMTP email sender with testbed-safe fallback."""

    def __init__(self, config: Dict[str, Any]):
        self._smtp_host = config.get("smtp_host") or os.environ.get("SMTP_HOST")
        self._smtp_port = int(config.get("smtp_port") or os.environ.get("SMTP_PORT", "587"))
        self._smtp_user = config.get("smtp_user") or os.environ.get("SMTP_USER")
        self._smtp_pass = config.get("smtp_pass") or os.environ.get("SMTP_PASS")
        self._sender = config.get("sender") or os.environ.get("SMTP_SENDER", "noreply@pgs.local")

    def _is_configured(self) -> bool:
        return bool(self._smtp_host and self._smtp_user and self._smtp_pass)

    def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send an email. Skips gracefully if SMTP is not configured."""
        recipient = payload.get("recipient")
        subject = payload.get("subject", "Notification")
        body_template = payload.get("body_template")
        template_vars = payload.get("template_vars", {})

        if not recipient or not isinstance(recipient, str) or "@" not in recipient:
            raise InvalidRecipient()

        if not self._is_configured():
            return {
                "result_status": "SUCCESS",
                "delivery_status": "skipped",
            }

        body = self._render_body(body_template, template_vars)

        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self._sender
            msg["To"] = recipient

            with smtplib.SMTP(self._smtp_host, self._smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self._smtp_user, self._smtp_pass)
                server.send_message(msg)

            return {
                "result_status": "SUCCESS",
                "delivery_status": "sent",
            }

        except (smtplib.SMTPException, OSError) as e:
            raise SmtpUnavailable(str(e)) from e

    def _render_body(self, template_name: str | None, template_vars: Dict[str, Any]) -> str:
        if template_name and template_name in TEMPLATES:
            return TEMPLATES[template_name].format(**template_vars)
        return str(template_vars)
