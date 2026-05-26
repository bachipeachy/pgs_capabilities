# CT Conformance Tests — governance atoms
# Test category: CT Conformance Tests
# Purpose: verify deterministic transformation correctness for governance CT atoms.
# Usage: python pgs_transforms/testbed/run_ct_conformance_governance_tests.py

# Bootstrap path before imports — CWD-independent via structure layer
from pgs_structure.structure.resolution import bootstrap
bootstrap()

from pgs_runtime.ct_executor import CTExecutionError
from pgs_transforms.implementation.transforms.atoms.ct_pure_validate_set_membership_v0 import (
    execute as validate_set_membership,
)
from pgs_transforms.implementation.transforms import (
    execute as lookup,
)
from pgs_transforms.implementation.transforms import (
    execute as validate_parameter_rules,
)


# ── CT_PURE_VALIDATE_SET_MEMBERSHIP_V0 ──────────────────────────

def test_set_membership_success():
    result = validate_set_membership(inputs={
        "value": "READ_RECORD",
        "allowed_set": ["READ_RECORD", "PROVISION_STANDARD_LICENSE", "PROVISION_PREMIUM_LICENSE"],
    })
    assert result["result_status"] == "SUCCESS"
    assert result["is_member"] is True


def test_set_membership_violation():
    try:
        validate_set_membership(inputs={
            "value": "DELETE_DATABASE",
            "allowed_set": ["READ_RECORD", "PROVISION_STANDARD_LICENSE"],
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_set_membership_empty_set():
    try:
        validate_set_membership(inputs={
            "value": "anything",
            "allowed_set": [],
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_set_membership_single_element():
    result = validate_set_membership(inputs={
        "value": "active",
        "allowed_set": ["active"],
    })
    assert result["result_status"] == "SUCCESS"
    assert result["is_member"] is True


def test_set_membership_missing_value():
    try:
        validate_set_membership(inputs={"allowed_set": ["a"]})
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_set_membership_missing_allowed_set():
    try:
        validate_set_membership(inputs={"value": "a"})
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


# ── CT_PURE_LOOKUP_V0 ───────────────────────────────────────────

def test_lookup_success():
    result = lookup(inputs={
        "key": "standard",
        "map": {
            "none": ["READ_RECORD"],
            "standard": ["READ_RECORD", "PROVISION_STANDARD_LICENSE"],
            "enterprise": ["READ_RECORD", "PROVISION_STANDARD_LICENSE", "PROVISION_PREMIUM_LICENSE"],
        },
    })
    assert result["result_status"] == "SUCCESS"
    assert result["result"] == ["READ_RECORD", "PROVISION_STANDARD_LICENSE"]


def test_lookup_violation():
    try:
        lookup(inputs={
            "key": "platinum",
            "map": {
                "none": ["READ_RECORD"],
                "standard": ["READ_RECORD", "PROVISION_STANDARD_LICENSE"],
            },
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_lookup_returns_object():
    result = lookup(inputs={
        "key": "config_a",
        "map": {
            "config_a": {"timeout": 30, "retries": 3},
        },
    })
    assert result["result_status"] == "SUCCESS"
    assert result["result"] == {"timeout": 30, "retries": 3}


def test_lookup_missing_key():
    try:
        lookup(inputs={"map": {"a": 1}})
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_lookup_missing_map():
    try:
        lookup(inputs={"key": "a"})
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


# ── CT_PURE_VALIDATE_PARAMETER_RULES_V0 ─────────────────────────

def test_parameter_rules_all_pass():
    result = validate_parameter_rules(inputs={
        "parameters": {"tier": "standard", "quantity": 50},
        "rules": [
            {"field": "tier", "op": "eq", "value": "standard"},
            {"field": "quantity", "op": "lte", "value": 100},
        ],
    })
    assert result["result_status"] == "SUCCESS"
    assert result["valid"] is True
    assert result["failed_rule"] is None


def test_parameter_rules_eq_violation():
    try:
        validate_parameter_rules(inputs={
            "parameters": {"tier": "premium", "quantity": 50},
            "rules": [
                {"field": "tier", "op": "eq", "value": "standard"},
            ],
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_parameter_rules_lte_violation():
    try:
        validate_parameter_rules(inputs={
            "parameters": {"tier": "standard", "quantity": 200},
            "rules": [
                {"field": "tier", "op": "eq", "value": "standard"},
                {"field": "quantity", "op": "lte", "value": 100},
            ],
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_parameter_rules_not_null_pass():
    result = validate_parameter_rules(inputs={
        "parameters": {"id": "rec_001"},
        "rules": [
            {"field": "id", "op": "not_null"},
        ],
    })
    assert result["result_status"] == "SUCCESS"
    assert result["valid"] is True


def test_parameter_rules_not_null_violation():
    try:
        validate_parameter_rules(inputs={
            "parameters": {"id": None},
            "rules": [
                {"field": "id", "op": "not_null"},
            ],
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_parameter_rules_not_null_missing_field():
    try:
        validate_parameter_rules(inputs={
            "parameters": {},
            "rules": [
                {"field": "id", "op": "not_null"},
            ],
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_parameter_rules_in_pass():
    result = validate_parameter_rules(inputs={
        "parameters": {"record_type": "license_pool"},
        "rules": [
            {"field": "record_type", "op": "in", "allowed": ["license_pool", "user_profile"]},
        ],
    })
    assert result["result_status"] == "SUCCESS"


def test_parameter_rules_in_violation():
    try:
        validate_parameter_rules(inputs={
            "parameters": {"record_type": "secret_data"},
            "rules": [
                {"field": "record_type", "op": "in", "allowed": ["license_pool", "user_profile"]},
            ],
        })
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_parameter_rules_gte():
    result = validate_parameter_rules(inputs={
        "parameters": {"quantity": 10},
        "rules": [
            {"field": "quantity", "op": "gte", "value": 1},
        ],
    })
    assert result["result_status"] == "SUCCESS"


def test_parameter_rules_neq():
    result = validate_parameter_rules(inputs={
        "parameters": {"status": "active"},
        "rules": [
            {"field": "status", "op": "neq", "value": "deleted"},
        ],
    })
    assert result["result_status"] == "SUCCESS"


def test_parameter_rules_empty_rules():
    result = validate_parameter_rules(inputs={
        "parameters": {"anything": "goes"},
        "rules": [],
    })
    assert result["result_status"] == "SUCCESS"
    assert result["valid"] is True


def test_parameter_rules_missing_parameters():
    try:
        validate_parameter_rules(inputs={"rules": []})
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


def test_parameter_rules_missing_rules():
    try:
        validate_parameter_rules(inputs={"parameters": {}})
        assert False, "Should have raised CTExecutionError"
    except CTExecutionError:
        pass


# ── Runner ───────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        # set membership
        test_set_membership_success,
        test_set_membership_violation,
        test_set_membership_empty_set,
        test_set_membership_single_element,
        test_set_membership_missing_value,
        test_set_membership_missing_allowed_set,
        # lookup
        test_lookup_success,
        test_lookup_violation,
        test_lookup_returns_object,
        test_lookup_missing_key,
        test_lookup_missing_map,
        # parameter rules
        test_parameter_rules_all_pass,
        test_parameter_rules_eq_violation,
        test_parameter_rules_lte_violation,
        test_parameter_rules_not_null_pass,
        test_parameter_rules_not_null_violation,
        test_parameter_rules_not_null_missing_field,
        test_parameter_rules_in_pass,
        test_parameter_rules_in_violation,
        test_parameter_rules_gte,
        test_parameter_rules_neq,
        test_parameter_rules_empty_rules,
        test_parameter_rules_missing_parameters,
        test_parameter_rules_missing_rules,
    ]

    for test in tests:
        test()
        print(f"  {test.__name__}")

    print(f"\nAll {len(tests)} governance atom tests passed.")
