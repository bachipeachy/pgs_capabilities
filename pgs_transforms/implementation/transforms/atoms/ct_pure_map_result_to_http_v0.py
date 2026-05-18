"""
ct_pure_map_result_to_http_v0.py — Map execution result to HTTP response.

Pure atom. Maps result_status to HTTP status code using a declared mapping.
"""

from typing import Any, Dict


def execute(*, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map execution result to HTTP response envelope.

    Inputs:
        execution_result: dict with at least 'status' and 'exit_reason_code'
        mapping: dict mapping result_status -> HTTP status code

    Returns:
        dict with http_status, response_body, result_status
    """
    execution_result = inputs.get("execution_result", {})
    mapping = inputs.get("mapping", {})

    # Extract the result_status from the execution result
    exec_status = execution_result.get("status", "BACKEND_ERROR")

    # Map to HTTP status
    if exec_status == "SUCCESS":
        result_status = "SUCCESS"
    elif exec_status == "FAILED":
        exit_reason = execution_result.get("exit_reason_code", "BACKEND_ERROR")
        # Map exit_reason_code to a result_status the mapping understands
        reason_to_status = {
            "EXIT_VIOLATION": "VIOLATION",
            "EXIT_NOT_FOUND": "NOT_FOUND",
            "EXIT_BACKEND_ERROR": "BACKEND_ERROR",
            "EXIT_REJECTED": "VIOLATION",
            "ADMISSION_DENIED": "VIOLATION",
            "NO_TRANSITION": "BACKEND_ERROR",
            "EXECUTION_ERROR": "BACKEND_ERROR",
            "GOVERNANCE_VIOLATION": "BACKEND_ERROR",
        }
        result_status = reason_to_status.get(exit_reason, "BACKEND_ERROR")
    else:
        result_status = "BACKEND_ERROR"

    http_status = mapping.get(result_status, 500)

    # Build response body
    response_body = {
        "status": exec_status,
        "exit_reason_code": execution_result.get("exit_reason_code"),
        "trace_id": execution_result.get("trace_id"),
        "result_payload": execution_result.get("result_payload", {}),
    }

    if execution_result.get("error_code"):
        response_body["error_code"] = execution_result["error_code"]
    if execution_result.get("message"):
        response_body["message"] = execution_result["message"]

    return {
        "http_status": http_status,
        "response_body": response_body,
        "result_status": result_status,
    }
