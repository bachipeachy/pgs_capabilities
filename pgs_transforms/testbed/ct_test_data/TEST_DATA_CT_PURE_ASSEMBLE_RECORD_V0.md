# TEST_DATA_CT_PURE_ASSEMBLE_RECORD_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_ASSEMBLE_RECORD_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_ASSEMBLE_RECORD_V0
  description: |
    Test record assembly from field values.
  target_artifact: CT_PURE_ASSEMBLE_RECORD_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_ASSEMBLE_RECORD_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_ASSEMBLE_RECORD_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0"
```

## Purpose

Test record assembly from field values.

## Test Cases

### Case 1: assemble_simple_record

**Description:** Assemble record from fields

```yaml
case_id: assemble_simple_record
expected_outcome: SUCCESS
bindings:
  fields:
    name: "Alice"
    age: 30
    active: true

expected:
  record:
    name: "Alice"
    age: 30
    active: true
```

### Case 2: assemble_nested_record

**Description:** Assemble record with nested fields

```yaml
case_id: assemble_nested_record
expected_outcome: SUCCESS
bindings:
  fields:
    user_id: "123"
    profile:
      email: "alice@example.com"
      role: "admin"

expected:
  record:
    user_id: "123"
    profile:
      email: "alice@example.com"
      role: "admin"
```
