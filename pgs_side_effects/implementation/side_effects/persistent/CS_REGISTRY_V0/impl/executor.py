"""
executor.py — Capability semantics for CS_REGISTRY_V0.
"""

from typing import Any, Dict

from pgs_side_effects.implementation.side_effects.persistent.CS_REGISTRY_V0.impl.backend import RegistryBackend
from pgs_side_effects.implementation.side_effects.persistent.CS_REGISTRY_V0.errors import (
    RegistryKeyExists,
    RegistryKeyNotFound,
    StorageUnavailable,
)


class RegistryExecutor:
    """Registry semantic executor."""

    def __init__(self, config: Dict[str, Any]):
        self._backend = RegistryBackend(config)

    def register(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new symbolic key with optional value enrichment."""
        if "key" not in payload:
            return {"result_status": "VIOLATION"}
        try:
            address = self._backend.register(
                key=payload["key"],
                target_cs=payload.get("target_cs"),
                target_ref=payload.get("target_ref"),
                value=payload.get("value"),
            )
            return {"result_status": "SUCCESS", "address": address}
        except RegistryKeyExists:
            return {"result_status": "ALREADY_EXISTS"}
        except StorageUnavailable:
            return {"result_status": "BACKEND_ERROR"}

    def resolve(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve a symbolic key or registry address."""
        if "key_or_address" not in payload:
            return {"result_status": "VIOLATION"}
        try:
            target_cs, target_ref = self._backend.resolve(payload["key_or_address"])
            return {"result_status": "SUCCESS", "target_cs": target_cs, "target_ref": target_ref}
        except RegistryKeyNotFound:
            return {"result_status": "NOT_FOUND"}
        except StorageUnavailable:
            return {"result_status": "BACKEND_ERROR"}

    def exists(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Check existence of a registry key or address."""
        if "key_or_address" not in payload:
            return {"result_status": "VIOLATION"}
        try:
            exists = self._backend.exists(payload["key_or_address"])
            return {"result_status": "SUCCESS", "exists": exists}
        except StorageUnavailable:
            return {"result_status": "BACKEND_ERROR"}

    def count(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Count active (non-tombstoned) registry entries."""
        try:
            count = self._backend.count()
            return {"result_status": "SUCCESS", "count": count}
        except StorageUnavailable:
            return {"result_status": "BACKEND_ERROR"}

    def deregister(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Deregister a registry entry (tombstone, does not delete storage)."""
        if "key_or_address" not in payload:
            return {"result_status": "VIOLATION"}
        try:
            removed = self._backend.deregister(payload["key_or_address"])
            if not removed:
                return {"result_status": "NOT_FOUND"}
            return {"result_status": "SUCCESS"}
        except StorageUnavailable:
            return {"result_status": "BACKEND_ERROR"}
