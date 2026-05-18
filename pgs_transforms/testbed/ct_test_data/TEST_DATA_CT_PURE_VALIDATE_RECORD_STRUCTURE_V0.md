# TEST_DATA_CT_PURE_VALIDATE_RECORD_STRUCTURE_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
  description: |
    Test record structure validation against schema.
  target_artifact: CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_VALIDATE_RECORD_STRUCTURE_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_VALIDATE_RECORD_STRUCTURE_V0"
```

## Purpose

Test record structure validation against schema.

## Test Cases

### Case 1: valid_record

**Description:** Validate record matching schema

```yaml
case_id: valid_record
bindings:
  record:
    name: "Alice"
    age: 30
  schema:
    name:
      required: true
      type: "string"
    age:
      required: true
      type: "integer"

expected:
  violations: []
```

### Case 2: invalid_record_missing_field

**Description:** Detect missing required field

```yaml
case_id: invalid_record_missing_field
bindings:
  record:
    name: "Bob"
  schema:
    name:
      required: true
      type: "string"
    age:
      required: true
      type: "integer"

expected:
  violations:
    - field: "age"
      rule: "required"
      message: "Field 'age' is required"
```
