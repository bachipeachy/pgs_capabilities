"""
CT_PURE_VALIDATE_PARAMETER_RULES_V0

Pure Capability Transform (Atom)

Purpose:
    Evaluate declarative parameter constraint rules against a parameter map.

Implementation:
    - Generic rule evaluator — no domain words
    - Supported ops: eq, neq, lte, gte, lt, gt, in, not_null
    - Returns SUCCESS if all rules pass
    - Raises VIOLATION on first failed rule with failed_rule detail
"""

from typing import Dict, Any

from pgs_runtime.ct_executor import CTExecutionError


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "parameters" not in inputs:
        raise CTExecutionError(
            "CT_PURE_VALIDATE_PARAMETER_RULES_V0: missing required input 'parameters'"
        )
    if "rules" not in inputs:
        raise CTExecutionError(
            "CT_PURE_VALIDATE_PARAMETER_RULES_V0: missing required input 'rules'"
        )

    parameters = inputs["parameters"]
    rules = inputs["rules"]

    if not isinstance(parameters, dict):
        raise CTExecutionError(
            f"CT_PURE_VALIDATE_PARAMETER_RULES_V0: parameters must be object, got {type(parameters).__name__}"
        )
    if not isinstance(rules, list):
        raise CTExecutionError(
            f"CT_PURE_VALIDATE_PARAMETER_RULES_V0: rules must be array, got {type(rules).__name__}"
        )

    for rule in rules:
        if not isinstance(rule, dict):
            continue

        field = rule.get("field")
        op = rule.get("op")

        if not field or not op:
            continue

        value = parameters.get(field)

        if not _evaluate_rule(value, op, rule):
            return {
                "valid": False,
                "failed_rule": rule,
            }

    return {
        "valid": True,
        "failed_rule": None,
    }


def _evaluate_rule(value: Any, op: str, rule: Dict[str, Any]) -> bool:
    """Evaluate a single constraint rule against a value."""

    if op == "not_null":
        return value is not None

    if op == "eq":
        return value == rule.get("value")

    if op == "neq":
        return value != rule.get("value")

    if op == "in":
        allowed = rule.get("allowed", [])
        return value in allowed

    # Numeric comparisons
    if op in ("lte", "gte", "lt", "gt"):
        rule_value = rule.get("value")
        if value is None or rule_value is None:
            return False
        try:
            num_value = float(value) if isinstance(value, str) else value
            num_rule = float(rule_value) if isinstance(rule_value, str) else rule_value
        except (ValueError, TypeError):
            return False

        if op == "lte":
            return num_value <= num_rule
        if op == "gte":
            return num_value >= num_rule
        if op == "lt":
            return num_value < num_rule
        if op == "gt":
            return num_value > num_rule

    # Unknown op — fail closed
    return False
