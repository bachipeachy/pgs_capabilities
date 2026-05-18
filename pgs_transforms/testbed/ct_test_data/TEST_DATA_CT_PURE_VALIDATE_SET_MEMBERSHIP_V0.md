# TEST_DATA_CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
  description: |
    Test set membership validation.
  target_artifact: CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_VALIDATE_SET_MEMBERSHIP_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0"
```

## Purpose

Test set membership validation.

## Test Cases

### Case 1: value_in_set

**Description:** Value is member of allowed set

```yaml
case_id: value_in_set
bindings:
  value: "active"
  allowed_set: ["active", "pending", "inactive"]

expected:
  is_member: true
```

### Case 2: value_not_in_set

**Description:** Value is not member of allowed set

```yaml
case_id: value_not_in_set
bindings:
  value: "deleted"
  allowed_set: ["active", "pending", "inactive"]

expected:
  is_member: false
```
