# TEST_DATA_CT_PURE_EXTRACT_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_EXTRACT_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_EXTRACT_V0
  description: |
    Test JSONPath-based value extraction from structured data.
  target_artifact: CT_PURE_EXTRACT_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_EXTRACT_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_EXTRACT_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_EXTRACT_V0"
```

## Purpose

Test JSONPath-based value extraction from structured data.

## Test Cases

### Case 1: extract_top_level_field

**Description:** Extract a top-level field from an object

```yaml
case_id: extract_top_level_field
expected_outcome: SUCCESS
bindings:
  from:
    name: "Alice"
    age: 30
  path: "name"
  type: "string"

expected:
  result: "Alice"
```

### Case 2: extract_nested_field

**Description:** Extract a nested field

```yaml
case_id: extract_nested_field
expected_outcome: SUCCESS
bindings:
  from:
    user:
      id: "123"
      role: "admin"
  path: "user.role"
  type: "string"

expected:
  result: "admin"
```

### Case 3: extract_nested_numeric

**Description:** Extract a nested numeric value

```yaml
case_id: extract_nested_numeric
expected_outcome: SUCCESS
bindings:
  from:
    config:
      timeout: 30
      retries: 3
  path: "config.timeout"
  type: "number"

expected:
  result: 30
```
