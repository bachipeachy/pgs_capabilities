"""
backend.py — Persistence backend for CS_REGISTRY_V0.

Path resolution:
- Entity-based (preferred): __pgs_store_entity__ → storage_structure_artifact.entity_stores[entity].path
  Used when RB declares storage_structure: and CC step declares store: field.
- Legacy (fallback): config["path"] — used for existing callers with explicit path policy.
Both modes are supported; entity-based takes precedence when store_entity is provided.
"""

import json
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple

from pgs_side_effects.implementation.side_effects.persistent.CS_REGISTRY_V0.errors import (
    RegistryKeyExists,
    RegistryKeyNotFound,
    StorageUnavailable,
)


class RegistryBackend:
    """File-based append-only registry backend with tombstone support."""

    def __init__(self, config: Dict):
        self._legacy_path_str: Optional[str] = config.get("path")
        self._storage_structure = config.get("storage_structure_artifact")
        self._module_data_root: Optional[str] = config.get("module_data_root")
        if self._module_data_root and "{{module_data_root}}" in self._module_data_root:
            # Template was not expanded — treat as absent
            self._module_data_root = None

        # Validate: at least one resolution mode must be available
        if not self._legacy_path_str and not (self._storage_structure and self._module_data_root):
            raise StorageUnavailable(
                "CS_REGISTRY_V0 requires either config['path'] or "
                "(storage_structure_artifact + module_data_root) for path resolution."
            )

    def _resolve_path(self, store_entity: Optional[str] = None) -> Path:
        """
        Resolve the registry file path.

        Entity-based resolution takes precedence when store_entity is provided
        and storage_structure_artifact is available. Falls back to config["path"].
        """
        if store_entity and self._storage_structure and self._module_data_root:
            core = self._storage_structure.get("frontmatter", {}).get("core", {})
            entity_stores = core.get("entity_stores", {})
            entity_config = entity_stores.get(store_entity)
            if entity_config:
                subpath = entity_config.get("path")
                if subpath:
                    full_path = Path(self._module_data_root) / subpath
                    try:
                        full_path.parent.mkdir(parents=True, exist_ok=True)
                        full_path.touch(exist_ok=True)
                    except Exception as e:
                        raise StorageUnavailable(str(e)) from e
                    return full_path

        # Fallback to legacy explicit path
        if self._legacy_path_str:
            try:
                p = Path(self._legacy_path_str)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.touch(exist_ok=True)
                return p
            except Exception as e:
                raise StorageUnavailable(str(e)) from e

        raise StorageUnavailable(
            f"Cannot resolve registry path for store_entity={store_entity!r}. "
            "Neither entity_stores entry nor config['path'] available."
        )

    def _load_all(self, path: Path) -> Dict[str, Dict]:
        """Load registry state. Last record per key wins; tombstoned keys excluded."""
        state: Dict[str, Dict] = {}
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    key = entry.get("key")
                    if key is None:
                        continue
                    if entry.get("tombstone") is True:
                        state.pop(key, None)
                    else:
                        state[key] = entry
            return state
        except Exception as e:
            raise StorageUnavailable(str(e)) from e

    def _find_entry(self, key_or_address: str, entries: Dict[str, Dict]) -> Dict | None:
        """Find entry by key or address."""
        for entry in entries.values():
            if entry["key"] == key_or_address or entry["address"] == key_or_address:
                return entry
        return None

    def register(self, key: str, target_cs: str | None = None, target_ref: str | None = None, value: dict | None = None, store_entity: Optional[str] = None) -> str:
        """Register a new key. Returns the generated address."""
        path = self._resolve_path(store_entity)
        entries = self._load_all(path)
        if key in entries:
            raise RegistryKeyExists(key)

        address = f"ADDR_{uuid.uuid4().hex}"
        record = {"key": key, "address": address}
        if target_cs is not None:
            record["target_cs"] = target_cs
        if target_ref is not None:
            record["target_ref"] = target_ref
        if value is not None:
            record.update(value)
        try:
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            return address
        except Exception as e:
            raise StorageUnavailable(str(e)) from e

    def resolve(self, key_or_address: str, store_entity: Optional[str] = None) -> Tuple[str, str]:
        """Resolve key or address to (target_cs, target_ref)."""
        path = self._resolve_path(store_entity)
        entries = self._load_all(path)
        entry = self._find_entry(key_or_address, entries)
        if entry:
            return entry.get("target_cs", ""), entry.get("target_ref", "")
        raise RegistryKeyNotFound(key_or_address)

    def exists(self, key_or_address: str, store_entity: Optional[str] = None) -> bool:
        """Check if key or address exists."""
        path = self._resolve_path(store_entity)
        entries = self._load_all(path)
        return self._find_entry(key_or_address, entries) is not None

    def count(self, store_entity: Optional[str] = None) -> int:
        """Count active (non-tombstoned) registry entries."""
        path = self._resolve_path(store_entity)
        return len(self._load_all(path))

    def deregister(self, key_or_address: str, store_entity: Optional[str] = None) -> bool:
        """Logical deregister via tombstone append."""
        path = self._resolve_path(store_entity)
        entries = self._load_all(path)
        entry = self._find_entry(key_or_address, entries)
        if not entry:
            return False

        tombstone = {
            "key": entry["key"],
            "address": entry["address"],
            "tombstone": True,
        }
        try:
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(tombstone) + "\n")
            return True
        except Exception as e:
            raise StorageUnavailable(str(e)) from e
