"""
CS_NAME_REGISTRY_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural mutation semantics and boundary correctness, not business semantics.
- Output shape: result_status always present
- READ idempotent; WRITE idempotent (last-write-wins)
- NOT_FOUND on READ for absent name
- VIOLATION on empty/missing name or non-list resource_addresses
- No metadata required (runtime accepts optional metadata)

Note: NameRegistryRuntime initializes the store file with "{}" if the path does
not exist. Tests use a TemporaryDirectory with a non-existent file path so the
runtime performs its own initialization (avoids empty-file JSON parse errors).
"""

import os
import tempfile

from pgs_side_effects.implementation.side_effects.persistent.CS_NAME_REGISTRY_V0.runtime import (
    NameRegistryRuntime,
)


def _make_runtime(tmpdir: str) -> NameRegistryRuntime:
    """Create a runtime backed by a fresh, non-existent store file inside tmpdir."""
    path = os.path.join(tmpdir, "name_registry.json")
    return NameRegistryRuntime(config={"path": path})


def test_write_read_result_shape():
    """WRITE then READ returns result_status and resource_addresses."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        write_result = rt.execute(op="WRITE", payload={
            "name": "alice",
            "resource_addresses": ["ADDR_001", "ADDR_002"],
        })
        assert write_result["result_status"] == "SUCCESS"
        assert write_result["success"] is True

        read_result = rt.execute(op="READ", payload={"name": "alice"})
        assert read_result["result_status"] == "SUCCESS"
        assert "resource_addresses" in read_result
        assert read_result["resource_addresses"] == ["ADDR_001", "ADDR_002"]


def test_write_idempotent_last_write_wins():
    """Second WRITE on same name overwrites; READ returns latest addresses."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        rt.execute(op="WRITE", payload={"name": "bob", "resource_addresses": ["ADDR_1"]})
        rt.execute(op="WRITE", payload={"name": "bob", "resource_addresses": ["ADDR_2"]})
        result = rt.execute(op="READ", payload={"name": "bob"})
        assert result["result_status"] == "SUCCESS"
        assert result["resource_addresses"] == ["ADDR_2"]


def test_read_not_found():
    """READ on absent name returns NOT_FOUND."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        result = rt.execute(op="READ", payload={"name": "ghost"})
        assert result["result_status"] == "NOT_FOUND"
        assert result["resource_addresses"] == []


def test_read_idempotent():
    """Repeated READ calls return identical results."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        rt.execute(op="WRITE", payload={"name": "carol", "resource_addresses": ["ADDR_X"]})
        r1 = rt.execute(op="READ", payload={"name": "carol"})
        r2 = rt.execute(op="READ", payload={"name": "carol"})
        assert r1 == r2


def test_violation_empty_name_on_write():
    """WRITE with empty name returns VIOLATION."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        result = rt.execute(op="WRITE", payload={"name": "", "resource_addresses": []})
        assert result["result_status"] == "VIOLATION"


def test_violation_non_list_resource_addresses():
    """WRITE with non-list resource_addresses returns VIOLATION."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        result = rt.execute(op="WRITE", payload={"name": "dave", "resource_addresses": "ADDR_1"})
        assert result["result_status"] == "VIOLATION"


def test_violation_empty_name_on_read():
    """READ with empty name returns VIOLATION."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        result = rt.execute(op="READ", payload={"name": ""})
        assert result["result_status"] == "VIOLATION"


def test_supported_operation_specs():
    """Runtime advertises READ and WRITE in supported_operation_specs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rt = _make_runtime(tmpdir)
        assert "READ" in rt.supported_operation_specs
        assert "WRITE" in rt.supported_operation_specs


if __name__ == "__main__":
    tests = [
        test_write_read_result_shape,
        test_write_idempotent_last_write_wins,
        test_read_not_found,
        test_read_idempotent,
        test_violation_empty_name_on_write,
        test_violation_non_list_resource_addresses,
        test_violation_empty_name_on_read,
        test_supported_operation_specs,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_NAME_REGISTRY_V0 contract tests passed.")
