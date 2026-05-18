"""
CS_MUTABLE_JSON_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural mutation semantics and boundary correctness, not business semantics.
- Output shape: result_status always present
- All read/update ops idempotent (GET, PUT, DELETE, EXISTS, LIST)
- NOT_FOUND on missing key
- VIOLATION on invalid key
- BACKEND_ERROR on unknown op
- __pgs_store_entity__ required in payload (protocol invariant)

Note: MutableJsonEngine requires storage_structure_artifact + module_data_root
injected at construction. Tests use a minimal mock structure to exercise the
boundary without coupling to any domain artifact.
"""

import tempfile
import os

from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.runtime import (
    MutableJsonRuntime,
)

_METADATA = {
    "capability": {
        "supported_operation_specs": ["READ", "WRITE", "DELETE", "EXISTS", "LIST_KEYS"]
    },
    "operations": {
        "operations": {
            "READ": {"handler": "read", "idempotent": True},
            "WRITE": {"handler": "write", "idempotent": True},
            "DELETE": {"handler": "delete", "idempotent": True},
            "EXISTS": {"handler": "exists", "idempotent": True},
            "LIST_KEYS": {"handler": "list_keys", "idempotent": True},
        }
    },
}

# Minimal mock storage structure — exercises entity path resolution
# without coupling to any real artifact
_MOCK_STRUCTURE = {
    "frontmatter": {
        "core": {
            "entity_stores": {
                "TEST_ENTITY": {"path": "test_store.json"}
            }
        }
    }
}


def _make_runtime(data_root: str) -> MutableJsonRuntime:
    return MutableJsonRuntime(
        config={
            "storage_structure_artifact": _MOCK_STRUCTURE,
            "module_data_root": data_root,
        },
        metadata=_METADATA,
    )


def _payload(op_fields: dict) -> dict:
    """Inject required __pgs_store_entity__ into every payload."""
    return {"__pgs_store_entity__": "TEST_ENTITY", **op_fields}


def test_write_read_result_shape():
    """WRITE then READ returns result_status + value with correct shape."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        put_result = rt.execute(op="WRITE", payload=_payload({"key": "k1", "value": {"x": 42}}))
        assert put_result["result_status"] == "SUCCESS"

        get_result = rt.execute(op="READ", payload=_payload({"key": "k1"}))
        assert get_result["result_status"] == "SUCCESS"
        assert "value" in get_result
        assert get_result["value"] == {"x": 42}


def test_write_idempotent_last_write_wins():
    """WRITE is idempotent — second write overwrites; READ returns latest value."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        rt.execute(op="WRITE", payload=_payload({"key": "k1", "value": "v1"}))
        rt.execute(op="WRITE", payload=_payload({"key": "k1", "value": "v2"}))
        result = rt.execute(op="READ", payload=_payload({"key": "k1"}))
        assert result["result_status"] == "SUCCESS"
        assert result["value"] == "v2"


def test_read_not_found():
    """READ on absent key returns NOT_FOUND."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        result = rt.execute(op="READ", payload=_payload({"key": "absent"}))
        assert result["result_status"] == "NOT_FOUND"


def test_delete_removes_key():
    """DELETE removes key; subsequent GET returns NOT_FOUND."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        rt.execute(op="WRITE", payload=_payload({"key": "k1", "value": "v1"}))
        del_result = rt.execute(op="DELETE", payload=_payload({"key": "k1"}))
        assert del_result["result_status"] == "SUCCESS"
        get_result = rt.execute(op="READ", payload=_payload({"key": "k1"}))
        assert get_result["result_status"] == "NOT_FOUND"


def test_exists_reflects_state():
    """EXISTS returns False before PUT and True after."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        before = rt.execute(op="EXISTS", payload=_payload({"key": "k1"}))
        assert before["result_status"] == "SUCCESS"
        assert before["exists"] is False

        rt.execute(op="WRITE", payload=_payload({"key": "k1", "value": "v"}))
        after = rt.execute(op="EXISTS", payload=_payload({"key": "k1"}))
        assert after["result_status"] == "SUCCESS"
        assert after["exists"] is True


def test_list_keys_returns_keys():
    """LIST_KEYS returns all stored keys."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        rt.execute(op="WRITE", payload=_payload({"key": "a", "value": 1}))
        rt.execute(op="WRITE", payload=_payload({"key": "b", "value": 2}))
        result = rt.execute(op="LIST_KEYS", payload=_payload({}))
        assert result["result_status"] == "SUCCESS"
        assert "keys" in result
        assert set(result["keys"]) == {"a", "b"}


def test_violation_on_empty_key():
    """PUT with empty-string key returns VIOLATION."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        result = rt.execute(op="WRITE", payload=_payload({"key": "", "value": "v"}))
        assert result["result_status"] == "VIOLATION"


def test_missing_store_entity_raises():
    """GET without __pgs_store_entity__ violates protocol — raises ValueError."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        raised = False
        try:
            rt.execute(op="READ", payload={"key": "k1"})
        except ValueError:
            raised = True
        assert raised, "Expected ValueError when __pgs_store_entity__ is absent"


def test_unknown_op_returns_backend_error():
    """Unknown operation verb returns BACKEND_ERROR."""
    with tempfile.TemporaryDirectory() as data_root:
        rt = _make_runtime(data_root)
        result = rt.execute(op="NONEXISTENT_OP", payload=_payload({}))
        assert result["result_status"] == "BACKEND_ERROR"


if __name__ == "__main__":
    tests = [
        test_write_read_result_shape,
        test_write_idempotent_last_write_wins,
        test_read_not_found,
        test_delete_removes_key,
        test_exists_reflects_state,
        test_list_keys_returns_keys,
        test_violation_on_empty_key,
        test_missing_store_entity_raises,
        test_unknown_op_returns_backend_error,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_MUTABLE_JSON_V0 contract tests passed.")
