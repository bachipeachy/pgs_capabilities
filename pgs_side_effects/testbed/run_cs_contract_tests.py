"""
CS Contract Test runner — analogous to CT Conformance Test runners.

Runs all CS boundary/contract tests across every CS implementation.
No pytest. No fixtures. Pure function tests with explicit failure reporting.

Test category: CS Contract Tests
Purpose: verify structural mutation semantics, protocol/runtime boundary
alignment, and admissibility envelope behavior.

Usage:
    cd <repo_root>
    source ../.venv/bin/activate
    python -m pgs_side_effects.testbed.run_cs_contract_tests
"""

import traceback

# --- Import all CS Contract Test modules ---

import pgs_side_effects.testbed.tests.test_cs_appendonly_jsonl as t_jsonl
import pgs_side_effects.testbed.tests.test_cs_mutable_json as t_mutable
import pgs_side_effects.testbed.tests.test_cs_registry as t_registry
import pgs_side_effects.testbed.tests.test_cs_name_registry as t_name_registry
import pgs_side_effects.testbed.tests.test_cs_send_email as t_email
import pgs_side_effects.testbed.tests.test_cs_workflow_gateway as t_gateway


# --- Test suites ---

SUITES = [
    ("CS_APPENDONLY_JSONL_V0", [
        t_jsonl.test_append_result_shape,
        t_jsonl.test_append_non_idempotent,
        t_jsonl.test_read_all_idempotent,
        t_jsonl.test_read_all_returns_appended_entries,
        t_jsonl.test_unknown_op_returns_backend_error,
        t_jsonl.test_metadata_contract_enforced,
    ]),
    ("CS_MUTABLE_JSON_V0", [
        t_mutable.test_write_read_result_shape,
        t_mutable.test_write_idempotent_last_write_wins,
        t_mutable.test_read_not_found,
        t_mutable.test_delete_removes_key,
        t_mutable.test_exists_reflects_state,
        t_mutable.test_list_keys_returns_keys,
        t_mutable.test_violation_on_empty_key,
        t_mutable.test_missing_store_entity_raises,
        t_mutable.test_unknown_op_returns_backend_error,
    ]),
    ("CS_REGISTRY_V0", [
        t_registry.test_register_result_shape,
        t_registry.test_register_non_idempotent_already_exists,
        t_registry.test_resolve_after_register,
        t_registry.test_resolve_idempotent,
        t_registry.test_resolve_not_found,
        t_registry.test_exists_reflects_registration,
        t_registry.test_deregister_tombstones_key,
        t_registry.test_deregister_absent_key_not_found,
        t_registry.test_violation_on_missing_key_field,
        t_registry.test_unknown_op_returns_backend_error,
    ]),
    ("CS_NAME_REGISTRY_V0", [
        t_name_registry.test_write_read_result_shape,
        t_name_registry.test_write_idempotent_last_write_wins,
        t_name_registry.test_read_not_found,
        t_name_registry.test_read_idempotent,
        t_name_registry.test_violation_empty_name_on_write,
        t_name_registry.test_violation_non_list_resource_addresses,
        t_name_registry.test_violation_empty_name_on_read,
        t_name_registry.test_supported_operation_specs,
    ]),
    ("CS_SEND_EMAIL_V0", [
        t_email.test_send_testbed_safe_skip,
        t_email.test_send_result_shape,
        t_email.test_violation_missing_recipient,
        t_email.test_violation_invalid_recipient_no_at,
        t_email.test_violation_recipient_not_string,
        t_email.test_unknown_op_returns_backend_error,
        t_email.test_metadata_contract_enforced,
    ]),
    ("CS_WORKFLOW_GATEWAY_V0", [
        t_gateway.test_execute_result_shape,
        t_gateway.test_executor_receives_workflow_code_and_payload,
        t_gateway.test_violation_missing_workflow_code,
        t_gateway.test_violation_missing_payload,
        t_gateway.test_not_found_on_unknown_workflow,
        t_gateway.test_backend_error_on_executor_exception,
        t_gateway.test_unknown_op_returns_backend_error,
        t_gateway.test_construction_requires_callable_executor,
    ]),
]


def run_all() -> None:
    total_passed = 0
    total_failed = 0
    failures = []

    for suite_name, tests in SUITES:
        print(f"\n{suite_name}")
        suite_passed = 0
        for test_fn in tests:
            try:
                test_fn()
                print(f"  [PASS] {test_fn.__name__}")
                suite_passed += 1
            except Exception:
                print(f"  [FAIL] {test_fn.__name__}")
                failures.append((suite_name, test_fn.__name__, traceback.format_exc()))
                total_failed += 1
        total_passed += suite_passed

    print(f"\n{'=' * 60}")
    print(f"CS contract tests: {total_passed} passed, {total_failed} failed")

    if failures:
        print("\nFailures:")
        for suite, name, tb in failures:
            print(f"\n  {suite} :: {name}")
            print(tb)
        raise SystemExit(1)

    print("All CS contract tests passed.")


if __name__ == "__main__":
    run_all()
