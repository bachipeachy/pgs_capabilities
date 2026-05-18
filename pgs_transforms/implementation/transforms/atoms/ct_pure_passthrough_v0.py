"""
ct_pure_passthrough_v0.py — Passthrough atom.

Returns the input value unchanged. Used for 1:1 payload mapping.
"""

from typing import Any, Dict


def execute(*, inputs: Dict[str, Any]) -> Any:
    """Pass through the input value unchanged."""
    return inputs.get("value")
