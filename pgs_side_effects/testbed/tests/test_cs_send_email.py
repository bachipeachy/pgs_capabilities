"""
CS_SEND_EMAIL_V0 — CS Contract Tests.

Test category: CS Contract Tests
Philosophy: verify structural mutation semantics and boundary correctness, not business semantics.
- Output shape: result_status always present
- Testbed-safe: SUCCESS with delivery_status "skipped" when SMTP not configured
- VIOLATION on invalid recipient (missing, non-string, missing @)
- BACKEND_ERROR on unknown op
- No SMTP connection attempted in testbed environment
"""

from pgs_side_effects.implementation.side_effects.external.CS_SEND_EMAIL_V0.runtime import (
    SendEmailRuntime,
)

_METADATA = {
    "capability": {
        "supported_operation_specs": ["SEND"]
    }
}

# Empty SMTP config — testbed-safe skip path is exercised
_CONFIG_NO_SMTP: dict = {}


def _make_runtime() -> SendEmailRuntime:
    return SendEmailRuntime(config=_CONFIG_NO_SMTP, metadata=_METADATA)


def test_send_testbed_safe_skip():
    """SEND without SMTP config returns SUCCESS with delivery_status 'skipped'."""
    rt = _make_runtime()
    result = rt.execute(op="SEND", payload={"recipient": "test@example.com"})
    assert result["result_status"] == "SUCCESS"
    assert result.get("delivery_status") == "skipped"


def test_send_result_shape():
    """SEND result always contains result_status and delivery_status."""
    rt = _make_runtime()
    result = rt.execute(op="SEND", payload={"recipient": "user@domain.org"})
    assert "result_status" in result
    assert "delivery_status" in result


def test_violation_missing_recipient():
    """SEND without recipient returns VIOLATION."""
    rt = _make_runtime()
    result = rt.execute(op="SEND", payload={})
    assert result["result_status"] == "VIOLATION"


def test_violation_invalid_recipient_no_at():
    """SEND with recipient missing '@' returns VIOLATION."""
    rt = _make_runtime()
    result = rt.execute(op="SEND", payload={"recipient": "notanemail"})
    assert result["result_status"] == "VIOLATION"


def test_violation_recipient_not_string():
    """SEND with non-string recipient returns VIOLATION."""
    rt = _make_runtime()
    result = rt.execute(op="SEND", payload={"recipient": 12345})
    assert result["result_status"] == "VIOLATION"


def test_unknown_op_returns_backend_error():
    """Unknown operation verb returns BACKEND_ERROR."""
    rt = _make_runtime()
    result = rt.execute(op="UNKNOWN_OP", payload={"recipient": "x@y.com"})
    assert result["result_status"] == "BACKEND_ERROR"


def test_metadata_contract_enforced():
    """Runtime rejects missing 'capability' in metadata at construction time."""
    raised = False
    try:
        SendEmailRuntime(config={}, metadata={})
    except AssertionError:
        raised = True
    assert raised, "Expected AssertionError for missing 'capability' in metadata"


if __name__ == "__main__":
    tests = [
        test_send_testbed_safe_skip,
        test_send_result_shape,
        test_violation_missing_recipient,
        test_violation_invalid_recipient_no_at,
        test_violation_recipient_not_string,
        test_unknown_op_returns_backend_error,
        test_metadata_contract_enforced,
    ]
    for t in tests:
        t()
        print(f"  {t.__name__}")
    print(f"\nAll {len(tests)} CS_SEND_EMAIL_V0 contract tests passed.")
