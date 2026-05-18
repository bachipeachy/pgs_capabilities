"""
CS_NAME_REGISTRY_V0 Runtime Implementation.

Persistent name-to-resource-addresses mapping store.

Operations: READ, WRITE
Result Status: SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR

CRITICAL:
- Last-write-wins semantics for WRITE
- Deterministic lookup for READ
- No internal IDs exposed (public projection only)
"""

import json
from pathlib import Path
from typing import Any


class NameRegistryRuntime:
    """Runtime for CS_NAME_REGISTRY_V0."""

    capability_kind = "CS"

    def __init__(self, config: dict[str, Any], metadata: dict[str, Any] | None = None, capability_code: str | None = None):
        """
        Initialize NameRegistryRuntime.

        Args:
            config: Must contain 'path' field (JSON file)
            metadata: Injected metadata (capability, operations) — stored for protocol compliance
            capability_code: CS code (default: CS_NAME_REGISTRY_V0)
        """
        self._capability_code = capability_code or "CS_NAME_REGISTRY_V0"
        self._metadata = metadata or {}

        if not isinstance(config, dict):
            raise ValueError("Config must be a dict")

        path = config.get("path")
        if not path:
            raise ValueError(f"{self._capability_code} requires 'path' in config")

        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)

        if not self._path.exists():
            self._path.write_text("{}", encoding="utf-8")

    @property
    def capability_code(self) -> str:
        return self._capability_code

    @property
    def supported_operation_specs(self) -> set[str]:
        return {"READ", "WRITE"}

    def execute(self, *, op: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Execute operation.

        Args:
            op: Operation name (READ, WRITE)
            payload: Operation payload

        Returns:
            Result dict with result_status and operation-specific fields
        """
        if op == "READ":
            return self._read(payload)
        elif op == "WRITE":
            return self._write(payload)
        else:
            return {
                "result_status": "VIOLATION",
                "error": f"Unsupported operation: {op}"
            }

    def _load_store(self) -> dict[str, Any]:
        """Load name registry from disk."""
        try:
            content = self._path.read_text(encoding="utf-8")
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Corrupt name registry at {self._path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load name registry: {e}")

    def _save_store(self, store: dict[str, Any]) -> None:
        """Save name registry to disk."""
        try:
            content = json.dumps(store, indent=2, ensure_ascii=False)
            self._path.write_text(content, encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to save name registry: {e}")

    def _read(self, payload: dict[str, Any]) -> dict[str, Any]:
        """READ operation — look up resource addresses for a name."""
        name = payload.get("name")
        if not isinstance(name, str) or not name:
            return {
                "result_status": "VIOLATION",
                "error": "name must be non-empty string"
            }
        try:
            store = self._load_store()
            if name in store:
                entry = store[name]
                return {
                    "result_status": "SUCCESS",
                    "resource_addresses": entry.get("resource_addresses", [])
                }
            else:
                return {
                    "result_status": "NOT_FOUND",
                    "resource_addresses": []
                }
        except Exception as e:
            return {
                "result_status": "BACKEND_ERROR",
                "error": str(e)
            }

    def _write(self, payload: dict[str, Any]) -> dict[str, Any]:
        """WRITE operation — register or update name → resource_addresses mapping."""
        name = payload.get("name")
        resource_addresses = payload.get("resource_addresses")

        if not isinstance(name, str) or not name:
            return {
                "result_status": "VIOLATION",
                "error": "name must be non-empty string"
            }
        if not isinstance(resource_addresses, list):
            return {
                "result_status": "VIOLATION",
                "error": "resource_addresses must be an array"
            }
        try:
            store = self._load_store()
            store[name] = {"resource_addresses": resource_addresses}
            self._save_store(store)
            return {
                "result_status": "SUCCESS",
                "success": True
            }
        except Exception as e:
            return {
                "result_status": "BACKEND_ERROR",
                "error": str(e),
                "success": False
            }
