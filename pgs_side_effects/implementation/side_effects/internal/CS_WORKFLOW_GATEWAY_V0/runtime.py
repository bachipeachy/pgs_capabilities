"""
runtime.py — Execution-only host for CS_WORKFLOW_GATEWAY_V0.

Governed by: CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

Wraps workflow_gateway.execute_workflow() as a governed CS operation.
Infrastructure-owned. Transport binds to this via runtime bindings.
"""

from typing import Any, Dict, Set


class WorkflowGatewayRuntime:
    """
    Execution-only host for CS_WORKFLOW_GATEWAY_V0.

    Delegates to workflow_gateway.execute_workflow() for actual execution.
    Returns execution result as a governed CS response.
    """

    capability_kind = "CS"
    _default_capability_code = "CS_WORKFLOW_GATEWAY_V0"

    def __init__(self, config: Dict[str, Any], metadata: Dict[str, Any], capability_code: str | None = None):
        """
        Parameters:
            config: Runtime configuration (must include 'workflow_executor')
            metadata: Injected metadata (capability, operations, schema)
            capability_code: Optional override for CS identity (metadata only)
        """
        # Defensive copy to prevent mutation
        self._metadata = dict(metadata)

        # Fail-fast validation
        assert isinstance(self._metadata, dict), "metadata must be dict"
        assert "capability" in self._metadata, "metadata must contain 'capability'"

        self._config = config
        self._capability_code = capability_code or self._default_capability_code
        self._default_rb = config.get("default_runtime_binding", "RB_CAPABILITY_BINDINGS_V0")

        # Enforce executor injection with interface contract
        self._workflow_executor = config.get("workflow_executor")
        assert self._workflow_executor is not None, "workflow_executor must be provided in config"
        assert callable(self._workflow_executor), "workflow_executor must be callable"

    @property
    def capability_code(self) -> str:
        return self._capability_code

    @property
    def supported_operation_specs(self) -> Set[str]:
        return {"EXECUTE"}

    def execute(self, *, op: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a validated CS operation.

        Supported ops:
        - EXECUTE: Invoke a workflow via the gateway
        """
        if op.upper() != "EXECUTE":
            return self._error("BACKEND_ERROR", f"Unsupported operation: {op}")

        workflow_code = payload.get("workflow_code")
        inner_payload = payload.get("payload")

        if not workflow_code:
            return self._error("VIOLATION", "Missing workflow_code")
        if inner_payload is None:
            return self._error("VIOLATION", "Missing payload")

        try:
            # Use injected workflow executor instead of importing from pgs_ingress
            result = self._workflow_executor(
                workflow_code=workflow_code,
                payload=inner_payload,
                runtime_binding=self._default_rb,
                mode="runtime",
            )

            return {
                "result_status": "SUCCESS" if result.status == "SUCCESS" else self._map_exit_reason(result.exit_reason_code),
                "execution_result": result.to_dict(),
            }

        except ValueError as e:
            if "Unknown workflow" in str(e):
                return self._error("NOT_FOUND", str(e))
            return self._error("BACKEND_ERROR", str(e))
        except Exception as e:
            return self._error("BACKEND_ERROR", str(e))

    @staticmethod
    def _map_exit_reason(exit_reason_code: str) -> str:
        """Map gateway exit_reason_code to CS result_status."""
        if exit_reason_code in ("EXIT_NOT_FOUND",):
            return "NOT_FOUND"
        return "BACKEND_ERROR"

    @staticmethod
    def _error(status: str, message: str | None = None) -> Dict[str, Any]:
        result: Dict[str, Any] = {"result_status": status}
        if message:
            result["message"] = message
        return result
