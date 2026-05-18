"""
backend.py — Persistence backend for CS_MUTABLE_JSON_V0.
"""

from typing import Dict, Any
import json
from pathlib import Path

from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.impl.utils import atomic_write_json
from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.errors import StorageCorrupt, StorageUnavailable


class JsonFileBackend:
    """
    Simple JSON-file backend.
    Entire dataset is read and written on each operation.
    """

    def __init__(self, path: str):
        self._path = Path(path)
        # Ensure the parent directory exists when the backend is initialized
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """Load entire JSON document."""
        if not self._path.exists():
            return {}

        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise StorageCorrupt("Root JSON must be an object")
                return data
        except json.JSONDecodeError as e:
            raise StorageCorrupt(str(e)) from e
        except OSError as e:
            raise StorageUnavailable(str(e)) from e

    def save(self, data: Dict[str, Any]) -> None:
        """Persist entire JSON document atomically."""
        try:
            atomic_write_json(self._path, data)
        except OSError as e:
            raise StorageUnavailable(str(e)) from e
