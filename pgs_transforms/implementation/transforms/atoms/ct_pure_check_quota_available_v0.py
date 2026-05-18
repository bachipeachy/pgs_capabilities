"""
CT_PURE_CHECK_QUOTA_AVAILABLE_V0

Pure Capability Transform (Atom)

Purpose:
    Check whether quota capacity is available (assigned count is less than quota limit).

Implementation:
    - Pure integer comparison
    - Returns boolean availability status
    - No exceptions (explicit output in all cases)
"""

from typing import Dict, Any


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Execute CT_PURE_CHECK_QUOTA_AVAILABLE_V0.

    Inputs:
        assigned_count (int): Current count of assigned items
        quota (int): Maximum allowed count (quota)

    Outputs:
        quota_available (bool): True if assigned_count < quota, False otherwise
    """
    if "assigned_count" not in inputs:
        raise ValueError(
            "CT_PURE_CHECK_QUOTA_AVAILABLE_V0: missing required input 'assigned_count'"
        )
    if "quota" not in inputs:
        raise ValueError(
            "CT_PURE_CHECK_QUOTA_AVAILABLE_V0: missing required input 'quota'"
        )

    assigned_count = inputs["assigned_count"]
    quota = inputs["quota"]

    if not isinstance(assigned_count, int):
        raise TypeError(
            f"CT_PURE_CHECK_QUOTA_AVAILABLE_V0: assigned_count must be int, got {type(assigned_count).__name__}"
        )

    if not isinstance(quota, int):
        raise TypeError(
            f"CT_PURE_CHECK_QUOTA_AVAILABLE_V0: quota must be int, got {type(quota).__name__}"
        )

    if quota < 0:
        raise ValueError(
            f"CT_PURE_CHECK_QUOTA_AVAILABLE_V0: quota must be non-negative, got {quota}"
        )

    # Pure comparison - return explicit boolean in all cases
    quota_available = assigned_count < quota

    return {
        "quota_available": quota_available
    }
