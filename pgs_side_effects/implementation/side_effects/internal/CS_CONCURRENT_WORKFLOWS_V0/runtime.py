"""
runtime.py — Execution-only host for CS_CONCURRENT_WORKFLOWS_V0.

Governed by: CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

Executes a declared set of workflows concurrently and collects all results.
Zero domain knowledge — the declaring CC provides all WF codes and payloads.

EXECUTE_CONCURRENT payload fields (resolved by dispatcher before delivery):
    workflows    — list of {code: FQDN, payload: object}; each code must be unique
    triggered_by — actor_id string

Contract invariants:
    - All workflows execute; VIOLATION in one does not halt peers.
    - Results correlated by code (workflow FQDN), NOT by array position.
    - Duplicate code values in a single invocation → VIOLATION.
    - Completion ordering is not guaranteed.

workflow_executor must be injected via config by the dispatcher.
Interface: executor(wf_fqdn: str, payload: dict) -> (result_status: str, surface: dict)
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Set


class ConcurrentWorkflowsRuntime:
    """
    Execution-only host for CS_CONCURRENT_WORKFLOWS_V0.

    Invokes all declared workflows and collects results correlated by code.
    All workflows run regardless of peer outcomes.
    """

    capability_kind = "CS"
    _default_capability_code = "CS_CONCURRENT_WORKFLOWS_V0"

    def __init__(
        self,
        config: Dict[str, Any],
        metadata: Dict[str, Any],
        capability_code: str | None = None,
    ):
        self._metadata = dict(metadata)
        assert isinstance(self._metadata, dict), "metadata must be dict"
        assert "capability" in self._metadata, "metadata must contain 'capability'"

        self._config = config
        self._capability_code = capability_code or self._default_capability_code

        self._workflow_executor = config.get("workflow_executor")
        assert self._workflow_executor is not None, "workflow_executor must be provided in config"
        assert callable(self._workflow_executor), "workflow_executor must be callable"

    @property
    def capability_code(self) -> str:
        return self._capability_code

    @property
    def supported_operation_specs(self) -> Set[str]:
        return {"EXECUTE_CONCURRENT"}

    def execute(self, *, op: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all declared workflows and return results correlated by code.

        Supported ops:
        - EXECUTE_CONCURRENT: invoke all workflows; collect results by code
        """
        if op.upper() != "EXECUTE_CONCURRENT":
            return {"result_status": "BACKEND_ERROR", "message": f"Unsupported operation: {op}"}

        workflows = payload.get("workflows")

        if not isinstance(workflows, list) or len(workflows) == 0:
            return {"result_status": "VIOLATION", "message": "workflows must be a non-empty list"}

        # Validate uniqueness of codes — duplicate codes are a VIOLATION
        codes = [entry.get("code") for entry in workflows if isinstance(entry, dict)]
        if len(codes) != len(set(codes)):
            return {"result_status": "VIOLATION", "message": "duplicate workflow codes in workflows list"}
        if any(c is None for c in codes):
            return {"result_status": "VIOLATION", "message": "each workflows entry must have a 'code' field"}

        def _invoke(entry: Dict[str, Any]) -> Dict[str, Any]:
            wf_code = entry.get("code")
            wf_payload = entry.get("payload") or {}
            try:
                result_status, outputs = self._workflow_executor(wf_code, wf_payload)
                return {"code": wf_code, "result_status": result_status, "outputs": outputs or {}}
            except Exception as exc:
                return {"code": wf_code, "result_status": "BACKEND_ERROR", "outputs": {}, "message": str(exc)}

        results = []
        all_succeeded = True

        with ThreadPoolExecutor() as pool:
            futures = [pool.submit(_invoke, entry) for entry in workflows]
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                if result["result_status"] != "SUCCESS":
                    all_succeeded = False

        overall_status = "SUCCESS" if all_succeeded else "PARTIAL_FAILURE"

        return {
            "result_status": overall_status,
            "results": results,
            "all_succeeded": all_succeeded,
        }
