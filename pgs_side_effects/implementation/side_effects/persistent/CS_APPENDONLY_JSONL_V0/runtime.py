"""
host.py — Execution-only host for CS_APPENDONLY_JSONL_V0.

Responsibilities:
- Execute append-only JSONL side-effect operations
- Translate backend errors into CEP-visible result_status values
"""

from typing import Any, Dict, Set

from pgs_side_effects.implementation.side_effects.persistent.CS_APPENDONLY_JSONL_V0.errors import (
    InvalidRecord,
    StorageCorrupt,
    StorageUnavailable,
)
from pgs_side_effects.implementation.side_effects.persistent.CS_APPENDONLY_JSONL_V0.impl.executor import (
    AppendOnlyJsonlEngine,
)


class AppendOnlyJsonlRuntime:
    """Execution-only host for CS_APPENDONLY_JSONL_V0."""

    capability_kind = "CS"
    _default_capability_code = "CS_APPENDONLY_JSONL_V0"

    def __init__(self, config: Dict[str, Any], metadata: Dict[str, Any], capability_code: str | None = None):
        """
        Parameters:
            config: Runtime configuration (e.g. {"path": "/tmp/appendonly.jsonl"})
            metadata: Injected metadata (capability, operations, schema)
            capability_code: Optional override for CS identity (metadata only)
        """
        # Defensive copy to prevent mutation
        self._metadata = dict(metadata)

        # Fail-fast validation
        assert isinstance(self._metadata, dict), "metadata must be dict"
        assert "capability" in self._metadata, "metadata must contain 'capability'"

        self._engine = AppendOnlyJsonlEngine(config)
        self._capability_code = capability_code or self._default_capability_code
        self._supported_operation_specs: Set[str] = set(
            self._metadata["capability"].get("supported_operation_specs", [])
        )

    @property
    def capability_code(self) -> str:
        return self._capability_code

    @property
    def supported_operation_specs(self) -> Set[str]:
        return self._supported_operation_specs

    def execute(self, *, op: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a validated CS operation."""
        try:
            handler = getattr(self._engine, op.lower(), None)
            if handler is None:
                return self._error("BACKEND_ERROR", f"No backend handler for op: {op}")
            return handler(payload)

        except InvalidRecord:
            return self._error("VIOLATION")

        except (StorageCorrupt, StorageUnavailable):
            return self._error("BACKEND_ERROR")

    @staticmethod
    def _error(status: str, message: str | None = None) -> Dict[str, Any]:
        result = {"result_status": status}
        if message:
            result["message"] = message
        return result
