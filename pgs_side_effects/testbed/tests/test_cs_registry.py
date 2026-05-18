"""
CS_REGISTRY_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural mutation semantics and boundary correctness, not business semantics.
- Output shape: result_status always present
- REGISTER is NOT idempotent — second REGISTER on same key yields ALREADY_EXISTS
- RESOLVE/EXISTS are idempotent
- DEREGISTER appends tombstone — key disappears from subsequent EXISTS
- NOT_FOUND on resolve/deregister of absent key
- VIOLATION on missing required field
- BACKEND_ERROR on unknown op
"""

import tempfile
import os

from pgs_side_effects.implementation.side_effects.persistent.CS_REGISTRY_V0.runtime import (
    RegistryRuntime,
)

_METADATA = {
    "capability": {
        "supported_operation_specs": ["REGISTER", "RESOLVE", "EXISTS", "DEREGISTER"]
    }
}


def _make_runtime(path: str) -> RegistryRuntime:
    return RegistryRuntime(config={"path": path}, metadata=_METADATA)


def test_register_result_shape():
    """REGISTER returns result_status and address."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        result = rt.execute(op="REGISTER", payload={
            "key": "actor::alice",
            "target_cs": "CS_MUTABLE_JSON_V0",
            "target_ref": "actors.json",
        })
        assert result["result_status"] == "SUCCESS"
        assert "address" in result
        assert result["address"].startswith("ADDR_")
    finally:
        os.unlink(path)


def test_register_non_idempotent_already_exists():
    """Second REGISTER on same key yields ALREADY_EXISTS."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        payload = {"key": "actor::bob", "target_cs": "CS_REGISTRY_V0", "target_ref": "ref"}
        r1 = rt.execute(op="REGISTER", payload=payload)
        r2 = rt.execute(op="REGISTER", payload=payload)
        assert r1["result_status"] == "SUCCESS"
        assert r2["result_status"] == "ALREADY_EXISTS"
    finally:
        os.unlink(path)


def test_resolve_after_register():
    """RESOLVE returns target_cs and target_ref for a registered key."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        rt.execute(op="REGISTER", payload={
            "key": "actor::carol",
            "target_cs": "CS_MUTABLE_JSON_V0",
            "target_ref": "actors.json",
        })
        result = rt.execute(op="RESOLVE", payload={"key_or_address": "actor::carol"})
        assert result["result_status"] == "SUCCESS"
        assert result["target_cs"] == "CS_MUTABLE_JSON_V0"
        assert result["target_ref"] == "actors.json"
    finally:
        os.unlink(path)


def test_resolve_idempotent():
    """RESOLVE is idempotent — repeated calls return same result."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        rt.execute(op="REGISTER", payload={"key": "k1", "target_cs": "CS_X", "target_ref": "ref"})
        r1 = rt.execute(op="RESOLVE", payload={"key_or_address": "k1"})
        r2 = rt.execute(op="RESOLVE", payload={"key_or_address": "k1"})
        assert r1 == r2
    finally:
        os.unlink(path)


def test_resolve_not_found():
    """RESOLVE on absent key returns NOT_FOUND."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        result = rt.execute(op="RESOLVE", payload={"key_or_address": "nonexistent"})
        assert result["result_status"] == "NOT_FOUND"
    finally:
        os.unlink(path)


def test_exists_reflects_registration():
    """EXISTS returns False before REGISTER and True after."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        before = rt.execute(op="EXISTS", payload={"key_or_address": "k1"})
        assert before["result_status"] == "SUCCESS"
        assert before["exists"] is False

        rt.execute(op="REGISTER", payload={"key": "k1", "target_cs": "CS_X", "target_ref": "r"})
        after = rt.execute(op="EXISTS", payload={"key_or_address": "k1"})
        assert after["result_status"] == "SUCCESS"
        assert after["exists"] is True
    finally:
        os.unlink(path)


def test_deregister_tombstones_key():
    """DEREGISTER via tombstone makes key absent from subsequent EXISTS."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        rt.execute(op="REGISTER", payload={"key": "k1", "target_cs": "CS_X", "target_ref": "r"})
        del_result = rt.execute(op="DEREGISTER", payload={"key_or_address": "k1"})
        assert del_result["result_status"] == "SUCCESS"
        exists = rt.execute(op="EXISTS", payload={"key_or_address": "k1"})
        assert exists["exists"] is False
    finally:
        os.unlink(path)


def test_deregister_absent_key_not_found():
    """DEREGISTER on absent key returns NOT_FOUND."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        result = rt.execute(op="DEREGISTER", payload={"key_or_address": "ghost"})
        assert result["result_status"] == "NOT_FOUND"
    finally:
        os.unlink(path)


def test_violation_on_missing_key_field():
    """REGISTER without 'key' field returns VIOLATION."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        result = rt.execute(op="REGISTER", payload={"target_cs": "CS_X"})
        assert result["result_status"] == "VIOLATION"
    finally:
        os.unlink(path)


def test_unknown_op_returns_backend_error():
    """Unknown operation verb returns BACKEND_ERROR."""
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        rt = _make_runtime(path)
        result = rt.execute(op="PURGE", payload={})
        assert result["result_status"] == "BACKEND_ERROR"
    finally:
        os.unlink(path)


if __name__ == "__main__":
    tests = [
        test_register_result_shape,
        test_register_non_idempotent_already_exists,
        test_resolve_after_register,
        test_resolve_idempotent,
        test_resolve_not_found,
        test_exists_reflects_registration,
        test_deregister_tombstones_key,
        test_deregister_absent_key_not_found,
        test_violation_on_missing_key_field,
        test_unknown_op_returns_backend_error,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_REGISTRY_V0 contract tests passed.")
