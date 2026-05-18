"""
host.py — Execution-only host for CS_MUTABLE_JSON_V0.

Responsibilities:
- Execute side-effect operations against the mutable JSON backend
- Translate backend errors into CEP-visible result_status values

Non-responsibilities (MOVED TO MACHINE):
- Protocol interpretation (operations.json)
- Capability contracts (CC mapping)
- Input presence validation
- Operation allow-listing

This host is intentionally dumb and stable.
"""

from typing import Any, Dict, Set

from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.errors import (
    InvalidKey,
    KeyNotFound,
    StorageCorrupt,
    StorageUnavailable,
)

from pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.impl.executor import (
    MutableJsonEngine,
)


class MutableJsonRuntime:
    """
    Execution-only host for CS_MUTABLE_JSON_V0.

    Machine invariants:
    - Called only with validated operation + payload
    - Protocol surface is enforced upstream
    """

    capability_kind = "CS"
    _default_capability_code = "CS_MUTABLE_JSON_V0"

    def __init__(self, config: Dict[str, Any], metadata: Dict[str, Any], capability_code: str | None = None):
        """
        Parameters:
            config: Runtime configuration (e.g. {"path": "/tmp/mutable.json"})
            metadata: Injected metadata (capability, operations, schema)
            capability_code: Optional override for CS identity (metadata only)
        """
        # Defensive copy to prevent mutation
        self._metadata = dict(metadata)

        # Fail-fast validation
        assert isinstance(self._metadata, dict), "metadata must be dict"
        assert "capability" in self._metadata, "metadata must contain 'capability'"
        assert "operations" in self._metadata, "metadata must contain 'operations'"

        self._engine = MutableJsonEngine(config)
        self._capability_code = capability_code or self._default_capability_code
        self._supported_operation_specs: Set[str] = set(
            self._metadata["capability"].get("supported_operation_specs", [])
        )
        self._ops_spec = self._metadata["operations"].get("operations", {})

    @property
    def capability_code(self) -> str:
        return self._capability_code

    @property
    def supported_operation_specs(self) -> Set[str]:
        return self._supported_operation_specs

    # ------------------------------------------------------------------
    # Execution entrypoint (machine-owned)
    # ------------------------------------------------------------------

    def execute(self, *, op: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a validated CS operation.

        Inputs:
        - op      : operation verb (e.g. PUT, GET, DELETE)
        - payload : validated inputs

        Output:
        - dict containing at minimum { result_status }
        """

        try:
            handler = getattr(self._engine, op.lower(), None)
            if handler is None:
                # Machine bug — protocol_validator allowed an op with no backend support
                return self._error(
                    "BACKEND_ERROR",
                    f"No backend handler for op: {op}",
                )

            return handler(payload)

        except InvalidKey:
            return self._error("VIOLATION")

        except KeyNotFound:
            return self._error("NOT_FOUND")

        except (StorageCorrupt, StorageUnavailable):
            return self._error("BACKEND_ERROR")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _error(status: str, message: str | None = None) -> Dict[str, Any]:
        result = {"result_status": status}
        if message:
            result["message"] = message
        return result
