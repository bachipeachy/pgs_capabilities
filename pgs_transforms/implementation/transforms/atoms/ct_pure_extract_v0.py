"""
CT_PURE_EXTRACT_V0

Pure Capability Transform (Atom)

Purpose:
    Extract values from nested data structures with type validation.

Implementation:
    - Navigate nested dicts via dot notation paths
    - Validate extracted value matches expected type
    - Pure extraction with no side effects
"""

from typing import Dict, Any


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Extract a value from nested data.

    Args:
        inputs: {
            "from": any - Data structure or context to extract from (matches contract)
            "path": str - Dot-notation path (e.g., "user.profile.email")
            "type": str - Expected type ("string", "number", "object", "array")
        }

    Returns:
        {
            "result": any - Extracted value (matches contract output name)
        }
    """
    # Validate inputs
    if "from" not in inputs:
        raise ValueError("CT_PURE_EXTRACT_V0: missing required input 'from'")
    if "path" not in inputs:
        raise ValueError("CT_PURE_EXTRACT_V0: missing required input 'path'")
    if "type" not in inputs:
        raise ValueError("CT_PURE_EXTRACT_V0: missing required input 'type'")

    source = inputs["from"]  # Contract declares 'from', not 'source'
    path = inputs["path"]
    expected_type = inputs["type"]

    if source is None:
        raise ValueError("CT_PURE_EXTRACT_V0: 'from' cannot be None")

    # Navigate path
    current = source
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            current = None
            break

    value = current

    # Type validation
    if value is not None:
        if expected_type == "string" and not isinstance(value, str):
            raise TypeError(
                f"CT_PURE_EXTRACT_V0: type mismatch at path '{path}': "
                f"expected string, got {type(value).__name__}"
            )
        elif expected_type == "number" and not isinstance(value, (int, float)):
            raise TypeError(
                f"CT_PURE_EXTRACT_V0: type mismatch at path '{path}': "
                f"expected number, got {type(value).__name__}"
            )
        elif expected_type == "object" and not isinstance(value, dict):
            raise TypeError(
                f"CT_PURE_EXTRACT_V0: type mismatch at path '{path}': "
                f"expected object, got {type(value).__name__}"
            )
        elif expected_type == "array" and not isinstance(value, list):
            raise TypeError(
                f"CT_PURE_EXTRACT_V0: type mismatch at path '{path}': "
                f"expected array, got {type(value).__name__}"
            )

    return {"result": value}  # Contract declares 'result', not 'value'
