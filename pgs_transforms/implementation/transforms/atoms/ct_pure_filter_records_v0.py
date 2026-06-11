"""
CT_PURE_FILTER_RECORDS_V0

Pure Capability Transform (Atom)

Purpose:
    Filter an array of record objects by declared field criteria.
    Supports exact-value matching and field-presence checks.

Implementation:
    - Iterates source array, testing each record against all filter criteria
    - Criterion value "present" means field must exist and be non-None
    - Any other criterion value means field must equal that value exactly
    - Returns extracted (filtered) array on success
    - Raises CTExecutionError when no records match (triggers VIOLATION at CC level)
    - Pure: no side effects, no state
"""

from typing import Dict, Any

from pgs_runtime.ct_executor import CTExecutionError

_PRESENT = "present"


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Filter an array of record objects by declared field criteria.

    Args:
        inputs: {
            "source": list  - Array of record objects to filter
            "filter": dict  - Field criteria: {"field": value} or {"field": "present"}
        }

    Returns:
        {"extracted": list} — filtered records that match all criteria

    Raises:
        CTExecutionError: if inputs malformed or no records match
    """
    if "source" not in inputs:
        raise CTExecutionError("CT_PURE_FILTER_RECORDS_V0: missing required input 'source'")
    if "filter" not in inputs:
        raise CTExecutionError("CT_PURE_FILTER_RECORDS_V0: missing required input 'filter'")

    source = inputs["source"]
    criteria = inputs["filter"]

    if not isinstance(source, list):
        raise CTExecutionError(
            f"CT_PURE_FILTER_RECORDS_V0: 'source' must be an array, got {type(source).__name__}"
        )
    if not isinstance(criteria, dict):
        raise CTExecutionError(
            f"CT_PURE_FILTER_RECORDS_V0: 'filter' must be an object, got {type(criteria).__name__}"
        )

    def matches(record: Any) -> bool:
        if not isinstance(record, dict):
            return False
        for field, criterion in criteria.items():
            value = record.get(field)
            if criterion == _PRESENT:
                if value is None:
                    return False
            else:
                if value != criterion:
                    return False
        return True

    extracted = [r for r in source if matches(r)]

    if not extracted:
        raise CTExecutionError(
            "CT_PURE_FILTER_RECORDS_V0: no records matched filter criteria"
        )

    return {"extracted": extracted}
