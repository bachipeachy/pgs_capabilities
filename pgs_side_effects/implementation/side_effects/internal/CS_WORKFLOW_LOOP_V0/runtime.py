"""
runtime.py — Execution-only host for CS_WORKFLOW_LOOP_V0.

Governed by: CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

Executes a finite sequence of governed WF invocations using a declarative
dispatch spec. Zero domain knowledge — the declaring CC provides all dispatch
logic as resolved input values.

EXECUTE_SEQUENCE payload fields (resolved by dispatcher before delivery):
    sequence          — list of items to iterate (e.g., slot descriptors)
    triggered_by      — actor_id string
    item_wf           — dict: {code, payload_fields, inject}
    item_sub_sequence — dict: {field, wf_dispatch: {key_field, mapping}, payload_fields}

workflow_executor must be injected via config by the dispatcher.
Interface: executor(wf_fqdn: str, payload: dict) -> (result_status: str, surface: dict)

Collatz loop semantics:
    For each item in sequence:
      1. Process item_sub_sequence (e.g., transactions) — dispatch sub-items by key-field
      2. Invoke item_wf (e.g., WF_PROPOSE_BLOCK_V0) with mapped item fields
    VIOLATION from any invocation halts immediately.
"""

from typing import Any, Dict, Set


class WorkflowLoopRuntime:
    """
    Execution-only host for CS_WORKFLOW_LOOP_V0.

    Iterates a sequence and invokes governed WFs per item and sub-item using
    a fully declarative dispatch spec. Zero domain knowledge.
    """

    capability_kind = "CS"
    _default_capability_code = "CS_WORKFLOW_LOOP_V0"

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
        return {"EXECUTE_SEQUENCE"}

    def execute(self, *, op: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a governed WF invocation sequence.

        Supported ops:
        - EXECUTE_SEQUENCE: iterate sequence, dispatch sub-items, invoke item WF
        """
        if op.upper() != "EXECUTE_SEQUENCE":
            return {"result_status": "BACKEND_ERROR", "message": f"Unsupported operation: {op}"}

        sequence = payload.get("sequence")
        item_wf_spec = payload.get("item_wf")
        item_sub_spec = payload.get("item_sub_sequence")

        if not isinstance(sequence, list):
            return {"result_status": "VIOLATION", "message": "sequence must be a list"}
        if not item_wf_spec or not isinstance(item_wf_spec, dict):
            return {"result_status": "VIOLATION", "message": "item_wf must be a dict"}

        item_wf_code_static = item_wf_spec.get("code")
        item_wf_dispatch = item_wf_spec.get("wf_dispatch")
        if not item_wf_code_static and not item_wf_dispatch:
            return {"result_status": "VIOLATION", "message": "item_wf must have 'code' or 'wf_dispatch'", "items_processed": 0, "sub_items_processed": 0}
        if item_wf_code_static and item_wf_dispatch:
            return {"result_status": "VIOLATION", "message": "item_wf must have exactly one of 'code' or 'wf_dispatch', not both", "items_processed": 0, "sub_items_processed": 0}

        items_processed = 0
        sub_items_processed = 0

        for item in sequence:
            # Process sub-sequence BEFORE item WF (transactions before block proposal)
            if item_sub_spec and isinstance(item_sub_spec, dict):
                sub_result = self._process_sub_sequence(item, item_sub_spec)
                if sub_result["result_status"] != "SUCCESS":
                    return {
                        "result_status": sub_result["result_status"],
                        "items_processed": items_processed,
                        "sub_items_processed": sub_items_processed,
                        "message": sub_result.get("message"),
                    }
                sub_items_processed += sub_result["sub_count"]

            # Invoke item WF — code (static) or wf_dispatch (key-field dispatch)
            if item_wf_dispatch:
                key_field = item_wf_dispatch.get("key_field")
                mapping = item_wf_dispatch.get("mapping") or {}
                key_value = item.get(key_field) if isinstance(item, dict) else None
                item_wf_code = mapping.get(key_value)
                if not item_wf_code:
                    return {
                        "result_status": "VIOLATION",
                        "message": f"No WF mapped for {key_field}={key_value!r}",
                        "items_processed": items_processed,
                        "sub_items_processed": sub_items_processed,
                    }
                payload_fields = item_wf_spec.get("payload_fields") or {}
                if payload_fields:
                    item_payload = self._build_payload(item, payload_fields)
                else:
                    item_payload = dict(item) if isinstance(item, dict) else {}
            else:
                item_wf_code = item_wf_code_static
                item_payload = self._build_payload(item, item_wf_spec.get("payload_fields") or {})

            item_payload.update(item_wf_spec.get("inject") or {})

            try:
                result_status, _ = self._workflow_executor(item_wf_code, item_payload)
            except Exception as exc:
                return {
                    "result_status": "BACKEND_ERROR",
                    "message": str(exc),
                    "items_processed": items_processed,
                    "sub_items_processed": sub_items_processed,
                }

            if result_status != "SUCCESS":
                return {
                    "result_status": "VIOLATION",
                    "items_processed": items_processed,
                    "sub_items_processed": sub_items_processed,
                }

            items_processed += 1

        return {
            "result_status": "SUCCESS",
            "items_processed": items_processed,
            "sub_items_processed": sub_items_processed,
        }

    def _process_sub_sequence(self, item: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
        """Process sub-items for a single sequence item using the dispatch spec."""
        field = spec.get("field")
        wf_dispatch = spec.get("wf_dispatch") or {}
        payload_fields = spec.get("payload_fields") or {}

        sub_seq = item.get(field, []) if field else []
        if not isinstance(sub_seq, list):
            return {
                "result_status": "VIOLATION",
                "sub_count": 0,
                "message": f"sub-sequence field '{field}' is not a list",
            }

        key_field = wf_dispatch.get("key_field")
        mapping = wf_dispatch.get("mapping") or {}
        sub_count = 0

        for sub_item in sub_seq:
            key_value = sub_item.get(key_field) if key_field else None
            wf_code = mapping.get(key_value) if key_value is not None else None
            if not wf_code:
                return {
                    "result_status": "VIOLATION",
                    "sub_count": sub_count,
                    "message": f"No WF mapped for {key_field}={key_value!r}",
                }

            # Build sub-item payload: explicit mapping or pass-through entire sub-item
            if payload_fields:
                sub_payload = self._build_payload(sub_item, payload_fields)
            else:
                sub_payload = dict(sub_item)

            try:
                result_status, _ = self._workflow_executor(wf_code, sub_payload)
            except Exception as exc:
                return {"result_status": "BACKEND_ERROR", "sub_count": sub_count, "message": str(exc)}

            if result_status != "SUCCESS":
                return {"result_status": "VIOLATION", "sub_count": sub_count}

            sub_count += 1

        return {"result_status": "SUCCESS", "sub_count": sub_count}

    @staticmethod
    def _build_payload(source: Dict[str, Any], payload_fields: Dict[str, str]) -> Dict[str, Any]:
        """Build a payload dict by mapping dest_field → source.get(source_field)."""
        return {dest: source.get(src) for dest, src in payload_fields.items()}
