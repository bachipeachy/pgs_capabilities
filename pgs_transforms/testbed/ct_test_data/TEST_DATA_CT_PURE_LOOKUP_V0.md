# TEST_DATA_CT_PURE_LOOKUP_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_LOOKUP_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_LOOKUP_V0
  description: |
    Test key-value lookup in mapping objects.
  target_artifact: CT_PURE_LOOKUP_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_LOOKUP_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_LOOKUP_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_LOOKUP_V0"
```

## Purpose

Test key-value lookup in mapping objects.

## Test Cases

### Case 1: lookup_string_value

**Description:** Look up a key with string value

```yaml
case_id: lookup_string_value
expected_outcome: SUCCESS
bindings:
  key: "status"
  map:
    status: "active"
    priority: "high"

expected:
  result: "active"
```

### Case 2: lookup_numeric_value

**Description:** Look up a key with numeric value

```yaml
case_id: lookup_numeric_value
expected_outcome: SUCCESS
bindings:
  key: "count"
  map:
    count: 100
    limit: 500

expected:
  result: 100
```

### Case 3: lookup_object_value

**Description:** Look up a key with object value

```yaml
case_id: lookup_object_value
expected_outcome: SUCCESS
bindings:
  key: "config"
  map:
    config:
      timeout: 30
      retries: 3
    enabled: true

expected:
  result:
    timeout: 30
    retries: 3
```

### Case 4: lookup_array_value

**Description:** Look up a key with array value

```yaml
case_id: lookup_array_value
expected_outcome: SUCCESS
bindings:
  key: "tags"
  map:
    tags: ["important", "urgent"]
    archived: false

expected:
  result: ["important", "urgent"]
```
