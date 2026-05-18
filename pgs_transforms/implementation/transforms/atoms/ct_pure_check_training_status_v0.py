"""
CT_PURE_CHECK_TRAINING_STATUS_V0

Pure Capability Transform (Atom)

Purpose:
    Check whether training is completed (eligibility check).

Implementation:
    - Pure boolean passthrough
    - Returns eligibility status
    - No exceptions (explicit output in all cases)
"""

from typing import Dict, Any


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Execute CT_PURE_CHECK_TRAINING_STATUS_V0.

    Inputs:
        training_completed (bool): True if training is finished

    Outputs:
        is_eligible (bool): True if training_completed is true
    """
    if "training_completed" not in inputs:
        raise ValueError(
            "CT_PURE_CHECK_TRAINING_STATUS_V0: missing required input 'training_completed'"
        )

    training_completed = inputs["training_completed"]

    if not isinstance(training_completed, bool):
        raise TypeError(
            f"CT_PURE_CHECK_TRAINING_STATUS_V0: training_completed must be bool, got {type(training_completed).__name__}"
        )

    # Pure passthrough - return explicit boolean in all cases
    is_eligible = training_completed

    return {
        "is_eligible": is_eligible
    }
