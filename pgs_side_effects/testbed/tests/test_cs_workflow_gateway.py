"""
CS_WORKFLOW_GATEWAY_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural mutation semantics and boundary correctness, not business semantics.

Executor interface (WorkflowGatewayRuntime):
    executor(wf_code: str, payload: dict) -> (result_status: str, surface: dict)

Contract invariants tested:
    - Output shape: result_status always present
    - workflow_executor must be injected and callable (enforced at construction)
    - VIOLATION on missing workflow_code or payload
    - BACKEND_ERROR on unknown op
    - NOT_FOUND when executor raises ValueError containing "not in vocab" or "No entry point"
    - BACKEND_ERROR on unexpected executor exception
    - Executor receives workflow_code and payload as positional arguments
"""

from pgs_side_effects.implementation.side_effects.internal.CS_WORKFLOW_GATEWAY_V0.runtime import (
    WorkflowGatewayRuntime,
)

_METADATA = {
    "capability": {
        "supported_operation_specs": ["EXECUTE"]
    }
}


def _make_runtime(executor_fn) -> WorkflowGatewayRuntime:
    return WorkflowGatewayRuntime(
        config={"workflow_executor": executor_fn},
        metadata=_METADATA,
    )


def _noop_executor(wf_code: str, payload: dict):
    return "SUCCESS", {}


# ── Construction guards ────────────────────────────────────────────────────────

def test_construction_requires_callable_executor():
    """Missing or non-callable workflow_executor raises AssertionError at construction."""
    raised = False
    try:
        WorkflowGatewayRuntime(config={}, metadata=_METADATA)
    except AssertionError:
        raised = True
    assert raised, "Expected AssertionError when workflow_executor is absent"

    raised = False
    try:
        WorkflowGatewayRuntime(config={"workflow_executor": "not_a_callable"}, metadata=_METADATA)
    except AssertionError:
        raised = True
    assert raised, "Expected AssertionError when workflow_executor is not callable"


# ── Input validation ───────────────────────────────────────────────────────────

def test_unknown_op_returns_backend_error():
    """Non-EXECUTE operation verb returns BACKEND_ERROR."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="RUN", payload={})
    assert result["result_status"] == "BACKEND_ERROR"


def test_violation_missing_workflow_code():
    """EXECUTE without workflow_code returns VIOLATION."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE", payload={"payload": {}})
    assert result["result_status"] == "VIOLATION"


def test_violation_missing_payload():
    """EXECUTE without payload field returns VIOLATION."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE", payload={"workflow_code": "wf::X"})
    assert result["result_status"] == "VIOLATION"


# ── Result shape ───────────────────────────────────────────────────────────────

def test_execute_result_shape():
    """EXECUTE returns result_status and execution_result on success."""
    rt = _make_runtime(_noop_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "blockchain::WF_TEST_V0",
        "payload": {"actor_id": "a1"},
    })
    assert result["result_status"] == "SUCCESS"
    assert "execution_result" in result


def test_executor_receives_workflow_code_and_payload():
    """EXECUTE passes workflow_code and payload as positional args to the executor."""
    captured = {}

    def _executor(wf_code: str, payload: dict):
        captured["workflow_code"] = wf_code
        captured["payload"] = payload
        return "SUCCESS", {}

    rt = _make_runtime(_executor)
    rt.execute(op="EXECUTE", payload={
        "workflow_code": "domain::WF_SOMETHING_V0",
        "payload": {"key": "val"},
    })
    assert captured["workflow_code"] == "domain::WF_SOMETHING_V0"
    assert captured["payload"] == {"key": "val"}


# ── Error routing ──────────────────────────────────────────────────────────────

def test_not_found_on_unknown_workflow():
    """EXECUTE returns NOT_FOUND when executor raises RuntimeError with 'not in vocab'."""
    def _executor(wf_code: str, payload: dict):
        raise RuntimeError(f"{wf_code} not in vocab")

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "wf::GHOST",
        "payload": {},
    })
    assert result["result_status"] == "NOT_FOUND"


def test_not_found_on_no_entry_point():
    """EXECUTE returns NOT_FOUND when executor raises RuntimeError with 'No entry point'."""
    def _executor(wf_code: str, payload: dict):
        raise RuntimeError(f"No entry point for {wf_code}")

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "wf::GHOST",
        "payload": {},
    })
    assert result["result_status"] == "NOT_FOUND"


def test_backend_error_on_executor_exception():
    """EXECUTE returns BACKEND_ERROR when executor raises unexpected exception."""
    def _executor(wf_code: str, payload: dict):
        raise RuntimeError("storage unavailable")

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "wf::X",
        "payload": {},
    })
    assert result["result_status"] == "BACKEND_ERROR"


def test_surface_dict_merged_into_execution_result():
    """Executor surface dict is merged into execution_result alongside status."""
    def _executor(wf_code: str, payload: dict):
        return "SUCCESS", {"actor_id": "A_abc123", "trace_id": "T_xyz"}

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "blockchain::WF_TEST_V0",
        "payload": {},
    })
    assert result["result_status"] == "SUCCESS"
    exec_result = result["execution_result"]
    assert exec_result["status"] == "SUCCESS"
    assert exec_result["actor_id"] == "A_abc123"
    assert exec_result["trace_id"] == "T_xyz"


# ── Runner ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_construction_requires_callable_executor,
        test_unknown_op_returns_backend_error,
        test_violation_missing_workflow_code,
        test_violation_missing_payload,
        test_execute_result_shape,
        test_executor_receives_workflow_code_and_payload,
        test_not_found_on_unknown_workflow,
        test_not_found_on_no_entry_point,
        test_backend_error_on_executor_exception,
        test_surface_dict_merged_into_execution_result,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_WORKFLOW_GATEWAY_V0 contract tests passed.")
