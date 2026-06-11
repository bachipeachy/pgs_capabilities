"""
executor.py — Capability semantics for CS_APPENDONLY_JSONL_V0.

Entity-based storage resolution:
- Paths resolved from STRUCTURE using store entity metadata
- storage_structure_artifact injected by RuntimeLoader from the RB's storage_structure reference
- module_data_root injected by RuntimeLoader from workflow context
- __pgs_store_entity__ injected per-operation by capability_pipeline from CC step store: field
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class AppendOnlyJsonlEngine:
    """
    Implements append-only JSONL semantics with entity-based path resolution.
    Storage paths are declared in STRUCTURE, not in RB policy.
    """

    def __init__(self, config: Dict[str, Any]):
        self._storage_structure = config.get("storage_structure_artifact")
        if not self._storage_structure:
            raise ValueError(
                "CS_APPENDONLY_JSONL_V0 requires storage_structure_artifact in config. "
                "RuntimeLoader must inject it from the RB storage_structure reference."
            )

        self._module_data_root = config.get("module_data_root")
        if not self._module_data_root:
            raise ValueError(
                "CS_APPENDONLY_JSONL_V0 requires module_data_root in config. "
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

    def append(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Append a record to the log."""
        path = self._resolve_storage_path(payload)

        sequence_counter = 0
        if path.exists():
            with open(path) as f:
                sequence_counter = sum(1 for _ in f)

        record = payload.get("record")
        stream_id = payload.get("stream_id")
        actor_id = payload.get("actor_id")

        timestamp = datetime.utcnow().isoformat()
        record_id = f"{timestamp}_{sequence_counter:06d}"
        sequence_number = sequence_counter + 1

        log_entry = {
            "record_id": record_id,
            "sequence_number": sequence_number,
            "timestamp": timestamp,
            "actor_id": actor_id,
            "stream_id": stream_id,
            "record": record,
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {
            "result_status": "SUCCESS",
            "record_id": record_id,
            "sequence_number": sequence_number,
        }

    def read_all(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Read all entries from the log, optionally filtered by stream_id."""
        path = self._resolve_storage_path(payload)
        stream_id = payload.get("stream_id")
        entries = []

        if path.exists():
            with open(path) as f:
                for line in f:
                    entry = json.loads(line)
                    if stream_id is None or entry.get("stream_id") == stream_id:
                        entries.append(entry)

        return {"result_status": "SUCCESS", "entries": entries}
