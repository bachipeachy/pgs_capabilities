"""
CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

Pure Capability Transform (Atom)

Purpose:
    Validate that a value is a member of a declared set.

Implementation:
    - Generic set membership check — no domain words
    - Returns SUCCESS with is_member=true if value is in allowed_set
    - Raises VIOLATION if value is not in allowed_set
"""

from typing import Dict, Any

from pgs_runtime.ct_executor import CTExecutionError


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "value" not in inputs:
        raise CTExecutionError(
            "CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: missing required input 'value'"
        )
    if "allowed_set" not in inputs:
        raise CTExecutionError(
            "CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: missing required input 'allowed_set'"
        )

    value = inputs["value"]
    allowed_set = inputs["allowed_set"]

    if not isinstance(allowed_set, list):
        raise CTExecutionError(
            f"CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: allowed_set must be array, got {type(allowed_set).__name__}"
        )

    is_member = value in allowed_set

    if not is_member:
        raise CTExecutionError(
            f"CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: value '{value}' is not in allowed_set {allowed_set}"
        )

    return {
        "result_status": "SUCCESS",
        "is_member": True,
    }
