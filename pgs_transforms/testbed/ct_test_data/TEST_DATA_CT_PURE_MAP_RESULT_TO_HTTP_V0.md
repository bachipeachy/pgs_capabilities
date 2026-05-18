# TEST_DATA_CT_PURE_MAP_RESULT_TO_HTTP_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_MAP_RESULT_TO_HTTP_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_MAP_RESULT_TO_HTTP_V0
  description: Validates HTTP response mapping for various execution result statuses including SUCCESS, FAILURE, custom status codes, and empty results.
  target_artifact: CT_PURE_MAP_RESULT_TO_HTTP_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_MAP_RESULT_TO_HTTP_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_MAP_RESULT_TO_HTTP_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_MAP_RESULT_TO_HTTP_V0"
```

## Purpose

Validates HTTP response mapping for various execution result statuses.

Tests cover:
- SUCCESS with data payload
- FAILURE with error message
- Custom status codes via mapping
- Empty result handling
- Complex nested data structures

---

## Test Cases

### Case 1: success_with_data

**Description:** Maps successful execution result with data payload

```yaml
case_id: success_with_data
bindings:
  execution_result:
    status: "SUCCESS"
    exit_reason_code: null
    trace_id: null
    result_payload:
      user_id: "usr_123"
      action: "created"
      timestamp: "2026-04-02T10:00:00Z"
  mapping:
    SUCCESS: 200
    FAILURE: 400
    ERROR: 500

expected:
  http_status: 200
  response_body:
    status: "SUCCESS"
    exit_reason_code: null
    trace_id: null
    result_payload:
      user_id: "usr_123"
      action: "created"
      timestamp: "2026-04-02T10:00:00Z"
  result_status: "SUCCESS"
```

### Case 2: failure_with_error

**Description:** Maps failed execution with error details

```yaml
case_id: failure_with_error
bindings:
  execution_result:
    status: "FAILED"
    exit_reason_code: "EXIT_VIOLATION"
    trace_id: null
    result_payload: {}
    error_code: "VALIDATION_ERROR"
    message: "Invalid email format"
  mapping:
    SUCCESS: 200
    VIOLATION: 400
    BACKEND_ERROR: 500

expected:
  http_status: 400
  response_body:
    status: "FAILED"
    exit_reason_code: "EXIT_VIOLATION"
    trace_id: null
    result_payload: {}
    error_code: "VALIDATION_ERROR"
    message: "Invalid email format"
  result_status: "VIOLATION"
```

### Case 3: error_with_custom_mapping

**Description:** Maps error status to custom HTTP code

```yaml
case_id: error_with_custom_mapping
bindings:
  execution_result:
    status: "FAILED"
    exit_reason_code: "EXIT_BACKEND_ERROR"
    trace_id: null
    result_payload: {}
    error_code: "INTERNAL_ERROR"
    message: "Database connection failed"
  mapping:
    SUCCESS: 200
    VIOLATION: 400
    BACKEND_ERROR: 503  # Service Unavailable

expected:
  http_status: 503
  response_body:
    status: "FAILED"
    exit_reason_code: "EXIT_BACKEND_ERROR"
    trace_id: null
    result_payload: {}
    error_code: "INTERNAL_ERROR"
    message: "Database connection failed"
  result_status: "BACKEND_ERROR"
```

### Case 4: success_empty_value

**Description:** Maps successful execution with empty result

```yaml
case_id: success_empty_value
bindings:
  execution_result:
    status: "SUCCESS"
    exit_reason_code: null
    trace_id: null
    result_payload: {}
  mapping:
    SUCCESS: 204  # No Content
    FAILURE: 400
    ERROR: 500

expected:
  http_status: 204
  response_body:
    status: "SUCCESS"
    exit_reason_code: null
    trace_id: null
    result_payload: {}
  result_status: "SUCCESS"
```

### Case 5: success_complex_nested

**Description:** Maps success with deeply nested data structure

```yaml
case_id: success_complex_nested
bindings:
  execution_result:
    status: "SUCCESS"
    exit_reason_code: null
    trace_id: null
    result_payload:
      transaction:
        id: "tx_abc123"
        type: "transfer"
        from:
          address: "0x1234..."
          balance: 100
        to:
          address: "0x5678..."
          balance: 200
        metadata:
          gas_used: 21000
          confirmations: 12
  mapping:
    SUCCESS: 200
    FAILURE: 400
    ERROR: 500

expected:
  http_status: 200
  response_body:
    status: "SUCCESS"
    exit_reason_code: null
    trace_id: null
    result_payload:
      transaction:
        id: "tx_abc123"
        type: "transfer"
        from:
          address: "0x1234..."
          balance: 100
        to:
          address: "0x5678..."
          balance: 200
        metadata:
          gas_used: 21000
          confirmations: 12
  result_status: "SUCCESS"
```

### Case 6: failure_validation_array

**Description:** Maps validation failure with multiple errors

```yaml
case_id: failure_validation_array
bindings:
  execution_result:
    status: "FAILED"
    exit_reason_code: "EXIT_VIOLATION"
    trace_id: null
    result_payload: {}
    error_code: "VALIDATION_ERROR"
    message: "Multiple validation errors"
  mapping:
    SUCCESS: 200
    VIOLATION: 422  # Unprocessable Entity
    BACKEND_ERROR: 500

expected:
  http_status: 422
  response_body:
    status: "FAILED"
    exit_reason_code: "EXIT_VIOLATION"
    trace_id: null
    result_payload: {}
    error_code: "VALIDATION_ERROR"
    message: "Multiple validation errors"
  result_status: "VIOLATION"
```

---

## Coverage Summary

- ✅ SUCCESS with data payload (simple + complex nested)
- ✅ FAILURE with error details (single + array)
- ✅ ERROR with custom mapping
- ✅ Empty value handling
- ✅ Custom HTTP status codes (200, 204, 400, 422, 500, 503)
- ✅ Nested object structures
- ✅ Array data in error details

**Total Cases:** 6
