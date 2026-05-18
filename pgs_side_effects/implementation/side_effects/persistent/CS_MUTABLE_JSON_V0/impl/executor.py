"""
executor.py — Capability semantics for CS_MUTABLE_JSON_V0.

Entity-based storage resolution:
- Paths resolved from STRUCTURE using store entity metadata (WALLET, TRANSACTION, ACTOR)
- storage_structure_artifact injected by RuntimeLoader from the RB's storage_structure reference
- module_data_root injected by RuntimeLoader from workflow context
- __pgs_store_entity__ injected per-operation by capability_pipeline from CC step store: field
"""

from typing import Any, Dict
from pathlib import Path

from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.impl.backend import JsonFileBackend
from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.impl.utils import validate_key
from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.errors import InvalidKey, KeyNotFound


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
        # GUARDRAIL 2: Require store entity metadata (from CC step)
        store_entity = payload.get("__pgs_store_entity__")
        if not store_entity:
            raise ValueError(
                "PROTOCOL VIOLATION: Missing __pgs_store_entity__ in payload. "
                "CC step must declare store: field for entity-based storage."
            )

        # Resolve entity to subpath from STRUCTURE
        entity_config = self._entity_storage_map.get(store_entity)
        if not entity_config:
            raise ValueError(
                f"PROTOCOL VIOLATION: Entity '{store_entity}' not found in STRUCTURE entity_stores. "
                f"Available entities: {list(self._entity_storage_map.keys())}"
            )

        # Get subpath from entity config
        subpath = entity_config.get("path")
        if not subpath:
            raise ValueError(
                f"PROTOCOL VIOLATION: Entity '{store_entity}' missing 'path' in STRUCTURE. "
                "Storage topology must declare paths for all entities."
            )

        # Construct full path: module_data_root + subpath
        full_path = Path(self._module_data_root) / subpath

        return full_path

    def _require_key(self, payload: Dict[str, Any]) -> str:
        """Extract and validate key from payload, raising InvalidKey if invalid."""
        key = payload.get("key")
        if not validate_key(key):
            raise InvalidKey()
        return key

    def read(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read value by key from entity-specific storage.

        PROTOCOL: Path resolved dynamically from store entity metadata.
        """
        # Resolve path from STRUCTURE using store entity
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        key = self._require_key(payload)
        data = backend.load()
        if key not in data:
            raise KeyNotFound()
        return {"result_status": "SUCCESS", "value": data[key]}

    def write(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Write key-value pair to entity-specific storage.

        PROTOCOL: Path resolved dynamically from store entity metadata.
        """
        # Resolve path from STRUCTURE using store entity
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        key = self._require_key(payload)
        value = payload.get("value")
        data = backend.load()
        data[key] = value
        backend.save(data)
        return {"result_status": "SUCCESS"}

    def delete(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete key from entity-specific storage.

        PROTOCOL: Path resolved dynamically from store entity metadata.
        """
        # Resolve path from STRUCTURE using store entity
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        key = self._require_key(payload)
        data = backend.load()
        if key not in data:
            raise KeyNotFound()
        del data[key]
        backend.save(data)
        return {"result_status": "SUCCESS"}

    def exists(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if key exists in entity-specific storage.

        PROTOCOL: Path resolved dynamically from store entity metadata.
        """
        # Resolve path from STRUCTURE using store entity
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        key = self._require_key(payload)
        data = backend.load()
        return {"result_status": "SUCCESS", "exists": key in data}

    def list_keys(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all keys in entity-specific storage.

        PROTOCOL: Path resolved dynamically from store entity metadata.
        """
        # Resolve path from STRUCTURE using store entity
        storage_path = self._resolve_storage_path(payload)
        backend = JsonFileBackend(str(storage_path))

        data = backend.load()
        return {"result_status": "SUCCESS", "keys": list(data.keys())}
