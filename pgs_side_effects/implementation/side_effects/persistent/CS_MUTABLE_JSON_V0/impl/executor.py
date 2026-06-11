"""
executor.py — Capability semantics for CS_MUTABLE_JSON_V0.

Entity-based storage resolution:
- Paths resolved from STRUCTURE using store entity metadata (WALLET, TRANSACTION, ACTOR)
- storage_structure_artifact injected by RuntimeLoader from the RB's storage_structure reference
- module_data_root injected by RuntimeLoader from workflow context
- __pgs_store_entity__ injected per-operation by capability_pipeline from CC step store: field
"""

import threading
from typing import Any, Dict
from pathlib import Path

from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.impl.backend import JsonFileBackend
from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.impl.utils import validate_key
from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.errors import InvalidKey, KeyNotFound

# Per-file threading locks — serialize concurrent load+save cycles on the same path.
_file_locks: dict[str, threading.Lock] = {}
_file_locks_registry_lock = threading.Lock()


def _get_file_lock(path: str) -> threading.Lock:
    with _file_locks_registry_lock:
        if path not in _file_locks:
            _file_locks[path] = threading.Lock()
        return _file_locks[path]


class MutableJsonEngine:
    """
    Implements mutable key-addressable JSON semantics with entity-based path resolution.
    Storage paths are declared in STRUCTURE, not in RB policy.
    """

    def __init__(self, config: Dict[str, Any]):
        self._storage_structure = config.get("storage_structure_artifact")
        if not self._storage_structure:
            raise ValueError(
                "CS_MUTABLE_JSON_V0 requires storage_structure_artifact in config. "
                "RuntimeLoader must inject it from the RB storage_structure reference."
            )

        self._module_data_root = config.get("module_data_root")
        if not self._module_data_root:
            raise ValueError(
                "CS_MUTABLE_JSON_V0 requires module_data_root in config. "
                "RuntimeLoader must inject it from workflow context."
            )

        core = self._storage_structure.get("frontmatter", {}).get("core", {})
        self._entity_storage_map = core.get("entity_stores", {})
        if not self._entity_storage_map:
            raise ValueError("STRUCTURE artifact missing entity_stores")

    def _resolve_storage_path(self, payload: Dict[str, Any]) -> Path:
        """
        Resolve storage path from STRUCTURE using store entity metadata.

        PROTOCOL: Store entity is injected by capability_pipeline from CC step metadata.

        Args:
            payload: Operation payload containing __pgs_store_entity__ metadata

        Returns:
            Resolved absolute path to storage file

        Raises:
            ValueError: If store entity missing or not found in STRUCTURE
        """
        store_entity = payload.get("__pgs_store_entity__")
        if not store_entity:
            raise ValueError(
                "PROTOCOL VIOLATION: Missing __pgs_store_entity__ in payload. "
                "CC step must declare store: field for entity-based storage."
            )

        entity_config = self._entity_storage_map.get(store_entity)
        if not entity_config:
            raise ValueError(
                f"PROTOCOL VIOLATION: Entity '{store_entity}' not found in STRUCTURE entity_stores. "
                f"Available entities: {list(self._entity_storage_map.keys())}"
            )

        subpath = entity_config.get("path")
        if not subpath:
            raise ValueError(
                f"PROTOCOL VIOLATION: Entity '{store_entity}' missing 'path' in STRUCTURE. "
                "Storage topology must declare paths for all entities."
            )

        return Path(self._module_data_root) / subpath

    def _require_key(self, payload: Dict[str, Any]) -> str:
        """Extract and validate key from payload, raising InvalidKey if invalid."""
        key = payload.get("key")
        if not validate_key(key):
            raise InvalidKey()
        return key

    def read(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Read value by key from entity-specific storage."""
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        key = self._require_key(payload)
        data = backend.load()
        if key not in data:
            raise KeyNotFound()
        return {"result_status": "SUCCESS", "value": data[key]}

    def write(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Write key-value pair to entity-specific storage."""
        storage_path = self._resolve_storage_path(payload)
        file_lock = _get_file_lock(str(storage_path))
        key = self._require_key(payload)
        value = payload.get("value")
        with file_lock:
            backend = JsonFileBackend(str(storage_path))
            data = backend.load()
            data[key] = value
            backend.save(data)
        return {"result_status": "SUCCESS"}

    def delete(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Delete key from entity-specific storage."""
        storage_path = self._resolve_storage_path(payload)
        file_lock = _get_file_lock(str(storage_path))
        key = self._require_key(payload)
        with file_lock:
            backend = JsonFileBackend(str(storage_path))
            data = backend.load()
            if key not in data:
                raise KeyNotFound()
            del data[key]
            backend.save(data)
        return {"result_status": "SUCCESS"}

    def exists(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Check if key exists in entity-specific storage."""
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        key = self._require_key(payload)
        data = backend.load()
        return {"result_status": "SUCCESS", "exists": key in data}

    def list_keys(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """List all keys in entity-specific storage."""
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        data = backend.load()
        return {"result_status": "SUCCESS", "keys": list(data.keys())}

    def list(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all records in entity-specific storage.

        Returns both keys (store keys) and records (full values).
        - $.capability_result.records — full record objects for CCs needing content
        - $.capability_result.keys   — store keys only, for CCs needing IDs
        Returns SUCCESS with empty records/keys when the store is empty.
        NOT_FOUND is reserved for keyed READ operations on a specific key that does not exist.
        """
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        data = backend.load()
        if not data:
            return {"result_status": "SUCCESS", "records": [], "keys": []}
        return {
            "result_status": "SUCCESS",
            "records": list(data.values()),
            "keys": list(data.keys()),
        }

    def delete_many(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a list of keys from entity-specific storage.

        Idempotent: NOT_FOUND per key is treated as already deleted (no error).
        Returns drained_count — number of keys that were actually present and removed.
        """
        storage_path = self._resolve_storage_path(payload)
        file_lock = _get_file_lock(str(storage_path))
        keys = payload.get("keys") or []
        with file_lock:
            backend = JsonFileBackend(str(storage_path))
            data = backend.load()
            drained_count = 0
            for key in keys:
                if key in data:
                    del data[key]
                    drained_count += 1
            backend.save(data)
        return {"result_status": "SUCCESS", "drained_count": drained_count}

    def update_where(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atomically update all records matching ALL filter conditions.

        Under a per-file lock: load → filter → apply updates → save.
        Concurrent callers on the same file are serialized — no interleaving.

        Args:
            filter:  {field: value, ...}  — ALL must match (AND semantics)
            updates: {field: value, ...}  — fields to set; None value removes the field

        Returns:
            SUCCESS  + matched_keys + updated_count  when ≥1 record matched
            VIOLATION + matched_keys=[] + updated_count=0  when no record matched
        """
        storage_path = self._resolve_storage_path(payload)
        file_lock = _get_file_lock(str(storage_path))

        filter_conditions: Dict[str, Any] = payload.get("filter") or {}
        updates: Dict[str, Any] = payload.get("updates") or {}

        with file_lock:
            backend = JsonFileBackend(str(storage_path))
            data = backend.load()

            matched_keys = [
                key for key, record in data.items()
                if isinstance(record, dict)
                and all(record.get(f) == v for f, v in filter_conditions.items())
            ]

            if not matched_keys:
                return {"result_status": "VIOLATION", "matched_keys": [], "updated_count": 0}

            for key in matched_keys:
                for field, value in updates.items():
                    if value is None:
                        data[key].pop(field, None)
                    else:
                        data[key][field] = value

            backend.save(data)

        return {
            "result_status": "SUCCESS",
            "matched_keys": matched_keys,
            "updated_count": len(matched_keys),
        }
