# TEST_DATA_CT_PURE_PASSTHROUGH_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_PASSTHROUGH_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_PASSTHROUGH_V0
  description: |
    Test that PASSTHROUGH returns input value unchanged for various data types.
  target_artifact: CT_PURE_PASSTHROUGH_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_PASSTHROUGH_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_PASSTHROUGH_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_PASSTHROUGH_V0"
```

## Purpose

Test that PASSTHROUGH returns input value unchanged for various data types.

## Test Cases

### Case 1: passthrough_string

**Description:** Pass through a string value

```yaml
case_id: passthrough_string
bindings:
  value: "hello world"

expected:
  value: "hello world"
```

### Case 2: passthrough_number

**Description:** Pass through a numeric value

```yaml
case_id: passthrough_number
bindings:
  value: 42

expected:
  value: 42
```

### Case 3: passthrough_object

**Description:** Pass through an object

```yaml
case_id: passthrough_object
bindings:
  value:
    key: "test"
    count: 123

expected:
  value:
    key: "test"
    count: 123
```

### Case 4: passthrough_array

**Description:** Pass through an array

```yaml
case_id: passthrough_array
bindings:
  value: [1, 2, 3]

expected:
  value: [1, 2, 3]
```

### Case 5: passthrough_boolean

**Description:** Pass through a boolean value

```yaml
case_id: passthrough_boolean
bindings:
  value: true

expected:
  value: true
```
