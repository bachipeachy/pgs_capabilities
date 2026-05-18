"""
CT_PURE_LOOKUP_V0

Pure Capability Transform (Atom)

Purpose:
    Look up a key in a declarative mapping and return the associated value.

Implementation:
    - Generic key-value lookup — no domain words
    - Returns SUCCESS with result if key is found
    - Raises VIOLATION if key is not found in map
"""

from typing import Dict, Any

from omnibachi.implementation.execution.machine.transforms.ct_executor import CTExecutionError


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "key" not in inputs:
        raise CTExecutionError(
            "CT_PURE_LOOKUP_V0: missing required input 'key'"
        )
    if "map" not in inputs:
        raise CTExecutionError(
            "CT_PURE_LOOKUP_V0: missing required input 'map'"
        )

    key = inputs["key"]
    mapping = inputs["map"]

    if not isinstance(mapping, dict):
        raise CTExecutionError(
            f"CT_PURE_LOOKUP_V0: map must be object, got {type(mapping).__name__}"
        )

    if key not in mapping:
        raise CTExecutionError(
            f"CT_PURE_LOOKUP_V0: key '{key}' not found in map"
        )

    return {
        "result": mapping[key],
    }
