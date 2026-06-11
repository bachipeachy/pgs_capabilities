"""
CS_CONCURRENT_WORKFLOWS_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural contract semantics and concurrency delivery.

Contract under test (CS_CONCURRENT_WORKFLOWS_V0.md §1 Intent):
  "Execute a declared set of workflows concurrently and collect all results."

Contract invariants tested:
  - All workflows execute regardless of peer outcomes (no short-circuit)
  - Results correlated by code (FQDN), NOT by array position
  - Duplicate code values → VIOLATION
  - Missing code field → VIOLATION
  - Empty workflows list → VIOLATION
  - EXECUTE_CONCURRENT is the only supported op; others → BACKEND_ERROR
  - workflow_executor must be injected and callable (enforced at construction)
  - CONCURRENCY: wall time for N parallel workers ≪ sum of individual durations

Concurrency conformance test (wall-time proof):
  Two workers each sleeping 3 seconds.
  Sequential execution would take ≥ 6 seconds.
  Concurrent execution must complete in < 5 seconds.
  Failure at ≥ 5 seconds means the contract is not being delivered.
"""

import time
from threading import Event

from pgs_side_effects.implementation.side_effects.internal.CS_CONCURRENT_WORKFLOWS_V0.runtime import (
    ConcurrentWorkflowsRuntime,
)

_METADATA = {
    "capability": {
        "supported_operation_specs": ["EXECUTE_CONCURRENT"]
    }
}


def _make_runtime(executor_fn) -> ConcurrentWorkflowsRuntime:
    return ConcurrentWorkflowsRuntime(
        config={"workflow_executor": executor_fn},
        metadata=_METADATA,
    )


def _noop_executor(wf_code: str, payload: dict):
    return "SUCCESS", {}


# ── Construction guards ────────────────────────────────────────────────────────

def test_construction_requires_executor():
    """Missing workflow_executor raises AssertionError at construction."""
    raised = False
    try:
        ConcurrentWorkflowsRuntime(config={}, metadata=_METADATA)
    except AssertionError:
        raised = True
    assert raised, "Expected AssertionError when workflow_executor is absent"


def test_construction_requires_callable_executor():
    """Non-callable workflow_executor raises AssertionError at construction."""
    raised = False
    try:
        ConcurrentWorkflowsRuntime(
            config={"workflow_executor": "not_a_callable"},
            metadata=_METADATA,
        )
    except AssertionError:
        raised = True
    assert raised, "Expected AssertionError when workflow_executor is not callable"


# ── Input validation ───────────────────────────────────────────────────────────

def test_unsupported_op_returns_backend_error():
    """Non-EXECUTE_CONCURRENT op returns BACKEND_ERROR."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="RUN", payload={"workflows": []})
    assert result["result_status"] == "BACKEND_ERROR"


def test_empty_workflows_returns_violation():
    """Empty workflows list returns VIOLATION."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={"workflows": []})
    assert result["result_status"] == "VIOLATION"


def test_missing_workflows_returns_violation():
    """Missing workflows field returns VIOLATION."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={})
    assert result["result_status"] == "VIOLATION"


def test_duplicate_code_returns_violation():
    """Duplicate workflow codes in a single invocation returns VIOLATION."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={
        "workflows": [
            {"code": "domain::WF_A_V0", "payload": {}},
            {"code": "domain::WF_A_V0", "payload": {}},
        ]
    })
    assert result["result_status"] == "VIOLATION"


def test_missing_code_field_returns_violation():
    """Workflow entry without 'code' field returns VIOLATION."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={
        "workflows": [{"payload": {}}]
    })
    assert result["result_status"] == "VIOLATION"


# ── Result shape ───────────────────────────────────────────────────────────────

def test_result_shape_on_success():
    """SUCCESS returns result_status, results array, and all_succeeded=True."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={
        "workflows": [
            {"code": "domain::WF_A_V0", "payload": {}},
            {"code": "domain::WF_B_V0", "payload": {}},
        ]
    })
    assert result["result_status"] == "SUCCESS"
    assert result["all_succeeded"] is True
    assert isinstance(result["results"], list)
    assert len(result["results"]) == 2
    codes = {r["code"] for r in result["results"]}
    assert codes == {"domain::WF_A_V0", "domain::WF_B_V0"}


def test_results_correlated_by_code_not_position():
    """Results are correlated by code field — lookup by code must be reliable."""
    outputs_by_code = {
        "domain::WF_A_V0": {"value": "alpha"},
        "domain::WF_B_V0": {"value": "beta"},
    }

    def _executor(wf_code: str, payload: dict):
        return "SUCCESS", outputs_by_code[wf_code]

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={
        "workflows": [
            {"code": "domain::WF_A_V0", "payload": {}},
            {"code": "domain::WF_B_V0", "payload": {}},
        ]
    })

    lookup = {r["code"]: r for r in result["results"]}
    assert lookup["domain::WF_A_V0"]["outputs"]["value"] == "alpha"
    assert lookup["domain::WF_B_V0"]["outputs"]["value"] == "beta"


def test_partial_failure_when_one_workflow_fails():
    """VIOLATION from one workflow → overall PARTIAL_FAILURE; peer still executes."""
    executed = set()

    def _executor(wf_code: str, payload: dict):
        executed.add(wf_code)
        if wf_code == "domain::WF_A_V0":
            return "VIOLATION", {}
        return "SUCCESS", {}

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={
        "workflows": [
            {"code": "domain::WF_A_V0", "payload": {}},
            {"code": "domain::WF_B_V0", "payload": {}},
        ]
    })

    # Both workflows must run regardless of peer outcome
    assert "domain::WF_A_V0" in executed
    assert "domain::WF_B_V0" in executed
    assert result["result_status"] == "PARTIAL_FAILURE"
    assert result["all_succeeded"] is False


def test_backend_error_on_executor_exception():
    """Executor exception → that workflow returns BACKEND_ERROR; peer still runs."""
    executed = set()

    def _executor(wf_code: str, payload: dict):
        executed.add(wf_code)
        if wf_code == "domain::WF_A_V0":
            raise RuntimeError("executor failure")
        return "SUCCESS", {}

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={
        "workflows": [
            {"code": "domain::WF_A_V0", "payload": {}},
            {"code": "domain::WF_B_V0", "payload": {}},
        ]
    })

    assert "domain::WF_A_V0" in executed
    assert "domain::WF_B_V0" in executed

    lookup = {r["code"]: r for r in result["results"]}
    assert lookup["domain::WF_A_V0"]["result_status"] == "BACKEND_ERROR"
    assert lookup["domain::WF_B_V0"]["result_status"] == "SUCCESS"
    assert result["result_status"] == "PARTIAL_FAILURE"


# ── Concurrency conformance (wall-time proof) ──────────────────────────────────

def test_execute_concurrent_delivers_concurrency():
    """
    CONCURRENCY CONFORMANCE — wall-time proof.

    Contract: "Execute a declared set of workflows concurrently"
    (CS_CONCURRENT_WORKFLOWS_V0.md §1 Intent)

    Two workers each block for 3 seconds.
    Sequential execution: ≥ 6 seconds.
    Concurrent execution: < 5 seconds.

    If this test fails (wall_time ≥ 5s), EXECUTE_CONCURRENT is not delivering
    its contract — the implementation is sequential, not concurrent.
    """
    _WORKER_SLEEP = 3.0
    _MAX_WALL_TIME = 5.0

    start_barrier = Event()

    def _blocking_executor(wf_code: str, payload: dict):
        start_barrier.wait()          # both workers held until both are ready
        time.sleep(_WORKER_SLEEP)
        return "SUCCESS", {"slept": _WORKER_SLEEP}

    rt = _make_runtime(_blocking_executor)

    # Release barrier after a short delay so both threads are waiting
    import threading
    threading.Timer(0.1, start_barrier.set).start()

    t0 = time.monotonic()
    result = rt.execute(op="EXECUTE_CONCURRENT", payload={
        "workflows": [
            {"code": "domain::WF_WORKER_A_V0", "payload": {}},
            {"code": "domain::WF_WORKER_B_V0", "payload": {}},
        ]
    })
    wall_time = time.monotonic() - t0

    assert result["result_status"] == "SUCCESS", (
        f"Expected SUCCESS, got {result['result_status']}"
    )
    assert wall_time < _MAX_WALL_TIME, (
        f"CONCURRENCY CONTRACT VIOLATED: wall_time={wall_time:.2f}s ≥ {_MAX_WALL_TIME}s. "
        f"Two {_WORKER_SLEEP}s workers ran sequentially instead of concurrently."
    )


# ── Runner ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_construction_requires_executor,
        test_construction_requires_callable_executor,
        test_unsupported_op_returns_backend_error,
        test_empty_workflows_returns_violation,
        test_missing_workflows_returns_violation,
        test_duplicate_code_returns_violation,
        test_missing_code_field_returns_violation,
        test_result_shape_on_success,
        test_results_correlated_by_code_not_position,
        test_partial_failure_when_one_workflow_fails,
        test_backend_error_on_executor_exception,
        test_execute_concurrent_delivers_concurrency,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_CONCURRENT_WORKFLOWS_V0 contract tests passed.")