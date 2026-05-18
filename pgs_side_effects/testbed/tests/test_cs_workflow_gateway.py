"""
CS_WORKFLOW_GATEWAY_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural mutation semantics and boundary correctness, not business semantics.
- Output shape: result_status always present
- workflow_executor must be injected and callable (enforced at construction)
- VIOLATION on missing workflow_code or payload
- BACKEND_ERROR on unknown op
- NOT_FOUND when executor raises ValueError("Unknown workflow...")
- Executor is injected — no real runtime is invoked here
"""

from pgs_side_effects.implementation.side_effects.internal.CS_WORKFLOW_GATEWAY_V0.runtime import (
    WorkflowGatewayRuntime,
)

_METADATA = {
    "capability": {
        "supported_operation_specs": ["EXECUTE"]
    }
}


# --- Minimal stub result for injected workflow executor ---

class _StubResult:
    """Minimal object satisfying WorkflowGatewayRuntime's result.status + to_dict() contract."""

    def __init__(self, status: str = "SUCCESS", exit_reason_code: str = "EXIT_SUCCESS"):
        self.status = status
        self.exit_reason_code = exit_reason_code

    def to_dict(self) -> dict:
        return {"status": self.status, "exit_reason_code": self.exit_reason_code}


def _make_runtime(executor_fn) -> WorkflowGatewayRuntime:
    return WorkflowGatewayRuntime(
        config={"workflow_executor": executor_fn},
        metadata=_METADATA,
    )


def test_execute_result_shape():
    """EXECUTE returns result_status and execution_result on success."""
    def _executor(**kwargs):
        return _StubResult(status="SUCCESS")

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "blockchain::WF_TEST_V0",
        "payload": {"actor_id": "a1"},
    })
    assert result["result_status"] == "SUCCESS"
    assert "execution_result" in result


def test_executor_receives_workflow_code_and_payload():
    """EXECUTE passes workflow_code and payload through to the injected executor."""
    captured = {}

    def _executor(**kwargs):
        captured.update(kwargs)
        return _StubResult(status="SUCCESS")

    rt = _make_runtime(_executor)
    rt.execute(op="EXECUTE", payload={
        "workflow_code": "domain::WF_SOMETHING_V0",
        "payload": {"key": "val"},
    })
    assert captured["workflow_code"] == "domain::WF_SOMETHING_V0"
    assert captured["payload"] == {"key": "val"}


def test_violation_missing_workflow_code():
    """EXECUTE without workflow_code returns VIOLATION."""
    rt = _make_runtime(lambda **kw: _StubResult())
    result = rt.execute(op="EXECUTE", payload={"payload": {}})
    assert result["result_status"] == "VIOLATION"


def test_violation_missing_payload():
    """EXECUTE without payload field returns VIOLATION."""
    rt = _make_runtime(lambda **kw: _StubResult())
    result = rt.execute(op="EXECUTE", payload={"workflow_code": "wf::X"})
    assert result["result_status"] == "VIOLATION"


def test_not_found_on_unknown_workflow():
    """EXECUTE returns NOT_FOUND when executor raises ValueError('Unknown workflow...')."""
    def _executor(**kwargs):
        raise ValueError("Unknown workflow: wf::GHOST")

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "wf::GHOST",
        "payload": {},
    })
    assert result["result_status"] == "NOT_FOUND"


def test_backend_error_on_executor_exception():
    """EXECUTE returns BACKEND_ERROR when executor raises unexpected exception."""
    def _executor(**kwargs):
        raise RuntimeError("storage unavailable")

    rt = _make_runtime(_executor)
    result = rt.execute(op="EXECUTE", payload={
        "workflow_code": "wf::X",
        "payload": {},
    })
    assert result["result_status"] == "BACKEND_ERROR"


def test_unknown_op_returns_backend_error():
    """Non-EXECUTE operation verb returns BACKEND_ERROR."""
    rt = _make_runtime(lambda **kw: _StubResult())
    result = rt.execute(op="RUN", payload={})
    assert result["result_status"] == "BACKEND_ERROR"


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


if __name__ == "__main__":
    tests = [
        test_execute_result_shape,
        test_executor_receives_workflow_code_and_payload,
        test_violation_missing_workflow_code,
        test_violation_missing_payload,
        test_not_found_on_unknown_workflow,
        test_backend_error_on_executor_exception,
        test_unknown_op_returns_backend_error,
        test_construction_requires_callable_executor,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_WORKFLOW_GATEWAY_V0 contract tests passed.")
