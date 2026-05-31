"""
backend.py — Persistence backend for CS_REGISTRY_V0.
"""

import json
import uuid
from pathlib import Path
from typing import Dict, Tuple

from pgs_side_effects.implementation.side_effects.persistent.CS_REGISTRY_V0.errors import (
    RegistryKeyExists,
    RegistryKeyNotFound,
    StorageUnavailable,
)


class RegistryBackend:
    """File-based append-only registry backend with tombstone support."""

    def __init__(self, config: Dict):
        try:
            self._path = Path(config["path"])
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.touch(exist_ok=True)
        except Exception as e:
            raise StorageUnavailable(str(e)) from e

    def _load_all(self) -> Dict[str, Dict]:
        """Load registry state. Last record per key wins; tombstoned keys excluded."""
        state: Dict[str, Dict] = {}
        try:
            with self._path.open("r", encoding="utf-8") as f:
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

    def register(self, key: str, target_cs: str | None = None, target_ref: str | None = None, value: dict | None = None) -> str:
        """Register a new key. Returns the generated address."""
        entries = self._load_all()
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
            with self._path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            return address
        except Exception as e:
            raise StorageUnavailable(str(e)) from e

    def resolve(self, key_or_address: str) -> Tuple[str, str]:
        """Resolve key or address to (target_cs, target_ref)."""
        entries = self._load_all()
        entry = self._find_entry(key_or_address, entries)
        if entry:
            return entry.get("target_cs", ""), entry.get("target_ref", "")
        raise RegistryKeyNotFound(key_or_address)

    def exists(self, key_or_address: str) -> bool:
        """Check if key or address exists."""
        entries = self._load_all()
        return self._find_entry(key_or_address, entries) is not None

    def count(self) -> int:
        """Count active (non-tombstoned) registry entries."""
        return len(self._load_all())

    def deregister(self, key_or_address: str) -> bool:
        """Logical deregister via tombstone append."""
        entries = self._load_all()
        entry = self._find_entry(key_or_address, entries)
        if not entry:
            return False

        tombstone = {
            "key": entry["key"],
            "address": entry["address"],
            "tombstone": True,
        }
        try:
            with self._path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(tombstone) + "\n")
            return True
        except Exception as e:
            raise StorageUnavailable(str(e)) from e
