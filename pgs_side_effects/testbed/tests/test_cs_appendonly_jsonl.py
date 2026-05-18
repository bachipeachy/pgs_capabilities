"""
CS_APPENDONLY_JSONL_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural mutation semantics and boundary correctness, not business semantics.
- Output shape: result_status always present
- Non-idempotency: APPEND creates new entries each call
- GET_ALL idempotency: repeated reads return same content
- Failure surface: VIOLATION on bad data, BACKEND_ERROR on unknown op
"""

import tempfile
import os

from pgs_side_effects.implementation.side_effects.persistent.CS_APPENDONLY_JSONL_V0.runtime import (
    AppendOnlyJsonlRuntime,
)

_METADATA = {
    "capability": {
        "supported_operation_specs": ["APPEND", "GET_ALL"]
    }
}


def _make_runtime(path: str) -> AppendOnlyJsonlRuntime:
    return AppendOnlyJsonlRuntime(config={"path": path}, metadata=_METADATA)


def test_append_result_shape():
    """APPEND returns result_status, record_id, sequence_number."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        result = rt.execute(op="APPEND", payload={
            "record": {"event": "test"},
            "stream_id": "stream_A",
            "actor_id": "actor_1",
        })
        assert result["result_status"] == "SUCCESS"
        assert "record_id" in result
        assert "sequence_number" in result
        assert isinstance(result["record_id"], str)
        assert isinstance(result["sequence_number"], int)
    finally:
        os.unlink(path)


def test_append_non_idempotent():
    """APPEND is NOT idempotent — same input produces distinct entries."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        payload = {"record": {"x": 1}, "stream_id": "s1", "actor_id": "a1"}
        r1 = rt.execute(op="APPEND", payload=payload)
        r2 = rt.execute(op="APPEND", payload=payload)
        assert r1["result_status"] == "SUCCESS"
        assert r2["result_status"] == "SUCCESS"
        # Distinct record identifiers
        assert r1["record_id"] != r2["record_id"]
        # Monotonically increasing sequence
        assert r2["sequence_number"] > r1["sequence_number"]
    finally:
        os.unlink(path)


def test_read_all_idempotent():
    """READ_ALL is idempotent — repeated reads produce same result."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        rt.execute(op="APPEND", payload={"record": {"v": 1}, "stream_id": "s1", "actor_id": "a1"})
        r1 = rt.execute(op="READ_ALL", payload={"stream_id": "s1"})
        r2 = rt.execute(op="READ_ALL", payload={"stream_id": "s1"})
        assert r1["result_status"] == "SUCCESS"
        assert r2["result_status"] == "SUCCESS"
        assert r1["entries"] == r2["entries"]
    finally:
        os.unlink(path)


def test_read_all_returns_appended_entries():
    """READ_ALL returns all previously APPENDed entries in the log."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        rt.execute(op="APPEND", payload={"record": {"n": 1}, "stream_id": "s1", "actor_id": "a1"})
        rt.execute(op="APPEND", payload={"record": {"n": 2}, "stream_id": "s1", "actor_id": "a1"})
        result = rt.execute(op="READ_ALL", payload={"stream_id": "s1"})
        assert result["result_status"] == "SUCCESS"
        assert "entries" in result
        assert len(result["entries"]) == 2
    finally:
        os.unlink(path)


def test_unknown_op_returns_backend_error():
    """Unknown operation verb returns BACKEND_ERROR — never silently succeeds."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        result = rt.execute(op="NONEXISTENT_OP", payload={})
        assert result["result_status"] == "BACKEND_ERROR"
    finally:
        os.unlink(path)


def test_metadata_contract_enforced():
    """Runtime rejects missing 'capability' key in metadata at construction time."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        raised = False
        try:
            AppendOnlyJsonlRuntime(config={"path": path}, metadata={})
        except AssertionError:
            raised = True
        assert raised, "Expected AssertionError for missing 'capability' in metadata"
    finally:
        os.unlink(path)


if __name__ == "__main__":
    tests = [
        test_append_result_shape,
        test_append_non_idempotent,
        test_read_all_idempotent,
        test_read_all_returns_appended_entries,
        test_unknown_op_returns_backend_error,
        test_metadata_contract_enforced,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_APPENDONLY_JSONL_V0 contract tests passed.")
