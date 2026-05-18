"""
CT_PURE_VALIDATE_RECORD_STRUCTURE_V0

Pure Capability Transform (Atom)

Purpose:
    Validate a record against a provided schema of field validation rules.

Implementation:
    - Generic record validator — no domain words
    - Schema defines field rules (type, required, pattern, min, max, etc.)
    - Returns result_status and violations list
"""

import re
from typing import Dict, Any, List


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "record" not in inputs:
        raise ValueError(
            "CT_PURE_VALIDATE_RECORD_STRUCTURE_V0: missing required input 'record'"
        )
    if "schema" not in inputs:
        raise ValueError(
            "CT_PURE_VALIDATE_RECORD_STRUCTURE_V0: missing required input 'schema'"
        )

    record = inputs["record"]
    schema = inputs["schema"]

    if not isinstance(record, dict):
        raise TypeError(
            f"CT_PURE_VALIDATE_RECORD_STRUCTURE_V0: record must be object, got {type(record).__name__}"
        )
    if not isinstance(schema, dict):
        raise TypeError(
            f"CT_PURE_VALIDATE_RECORD_STRUCTURE_V0: schema must be object, got {type(schema).__name__}"
        )

    violations: List[Dict[str, str]] = []

    for field_name, rules in schema.items():
        if not isinstance(rules, dict):
            continue

        value = record.get(field_name)

        # Check required
        if rules.get("required", False) and (value is None or value == ""):
            violations.append({
                "field": field_name,
                "rule": "required",
                "message": f"Field '{field_name}' is required"
            })
            continue

        # Skip further validation if field is absent and not required
        if value is None:
            continue

        # Check type
        expected_type = rules.get("type")
        if expected_type:
            if not _check_type(value, expected_type):
                violations.append({
                    "field": field_name,
                    "rule": "type",
                    "message": f"Field '{field_name}' must be {expected_type}, got {type(value).__name__}"
                })
                continue

        # Check pattern (regex)
        pattern = rules.get("pattern")
        if pattern and isinstance(value, str):
            if not re.fullmatch(pattern, value):
                violations.append({
                    "field": field_name,
                    "rule": "pattern",
                    "message": f"Field '{field_name}' does not match pattern '{pattern}'"
                })

        # Check min_value
        min_value = rules.get("min_value")
        if min_value is not None:
            numeric_value = _to_numeric(value)
            if numeric_value is not None and numeric_value < min_value:
                violations.append({
                    "field": field_name,
                    "rule": "min_value",
                    "message": f"Field '{field_name}' must be >= {min_value}, got {numeric_value}"
                })

        # Check max_value
        max_value = rules.get("max_value")
        if max_value is not None:
            numeric_value = _to_numeric(value)
            if numeric_value is not None and numeric_value > max_value:
                violations.append({
                    "field": field_name,
                    "rule": "max_value",
                    "message": f"Field '{field_name}' must be <= {max_value}, got {numeric_value}"
                })

        # Check min_length
        min_length = rules.get("min_length")
        if min_length is not None and isinstance(value, str):
            if len(value) < min_length:
                violations.append({
                    "field": field_name,
                    "rule": "min_length",
                    "message": f"Field '{field_name}' must be at least {min_length} characters"
                })

        # Check max_length
        max_length = rules.get("max_length")
        if max_length is not None and isinstance(value, str):
            if len(value) > max_length:
                violations.append({
                    "field": field_name,
                    "rule": "max_length",
                    "message": f"Field '{field_name}' must be at most {max_length} characters"
                })

        # Check cross-field constraint: lte_field (value must be <= another field's value)
        lte_field = rules.get("lte_field")
        if lte_field and lte_field in record:
            numeric_value = _to_numeric(value)
            other_value = _to_numeric(record[lte_field])
            if numeric_value is not None and other_value is not None:
                if numeric_value > other_value:
                    violations.append({
                        "field": field_name,
                        "rule": "lte_field",
                        "message": f"Field '{field_name}' must be <= '{lte_field}'"
                    })

    return {
        "violations": violations
    }


def _check_type(value: Any, expected_type: str) -> bool:
    """Check if value matches the expected type string."""
    if expected_type == "string":
        return isinstance(value, str)
    elif expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    elif expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    elif expected_type == "boolean":
        return isinstance(value, bool)
    elif expected_type == "object":
        return isinstance(value, dict)
    elif expected_type == "array":
        return isinstance(value, list)
    elif expected_type == "integer_string":
        # String that represents a non-negative integer
        if not isinstance(value, str):
            return False
        try:
            int(value)
            return True
        except ValueError:
            return False
    elif expected_type == "hex_string":
        # 0x-prefixed hex string
        if not isinstance(value, str):
            return False
        if not value.startswith("0x") and not value.startswith("0X"):
            return False
        try:
            bytes.fromhex(value[2:])
            return True
        except ValueError:
            return False
    return True


def _to_numeric(value: Any):
    """Convert value to numeric for comparison, or return None."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None
    return None
