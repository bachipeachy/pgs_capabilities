"""
CT_PURE_EVALUATE_INACTIVITY_V0 — Evaluate license inactivity.

Governed by: CAPABILITY_TRANSFORMS_CONSTITUTION_V0

Pure transform: same input always yields same output.
No side effects, no state.

Always returns a structured result — never raises for business outcomes.
"""

from typing import Dict, Any
from datetime import datetime, timezone


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Evaluate whether a license is inactive based on last usage.

    Inputs:
        last_active_date (str): ISO 8601 datetime string
        threshold_days (int): Number of days before considered inactive
        current_date (str): ISO 8601 datetime string representing "now"

    Outputs:
        is_inactive (bool): True if days_inactive >= threshold_days
        days_inactive (int): Number of days since last_active_date
    """
    last_active_str = inputs.get("last_active_date")
    threshold_days = inputs.get("threshold_days", 30)
    current_date_str = inputs.get("current_date")

    if not last_active_str:
        return {"is_inactive": True, "days_inactive": 999}

    def _parse_iso(s: str) -> datetime:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    try:
        last_active = _parse_iso(last_active_str)
        if current_date_str:
            current_dt = _parse_iso(current_date_str)
        else:
            current_dt = datetime.now(timezone.utc)
        days_inactive = (current_dt - last_active).days
    except (ValueError, TypeError):
        days_inactive = 999

    is_inactive = days_inactive >= threshold_days

    return {
        "is_inactive": is_inactive,
        "days_inactive": days_inactive,
    }