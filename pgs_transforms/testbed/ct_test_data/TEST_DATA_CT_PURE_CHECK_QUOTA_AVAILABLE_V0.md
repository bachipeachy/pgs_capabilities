# TEST_DATA_CT_PURE_CHECK_QUOTA_AVAILABLE_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_CHECK_QUOTA_AVAILABLE_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_CHECK_QUOTA_AVAILABLE_V0
  description: |
    Test quota availability checking logic.
  target_artifact: CT_PURE_CHECK_QUOTA_AVAILABLE_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_CHECK_QUOTA_AVAILABLE_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_CHECK_QUOTA_AVAILABLE_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_CHECK_QUOTA_AVAILABLE_V0"
```

## Purpose

Test quota availability checking logic.

## Test Cases

### Case 1: quota_available

**Description:** Assigned count is below quota

```yaml
case_id: quota_available
bindings:
  assigned_count: 5
  quota: 10

expected:
  quota_available: true
```

### Case 2: quota_exceeded

**Description:** Assigned count equals or exceeds quota

```yaml
case_id: quota_exceeded
bindings:
  assigned_count: 10
  quota: 10

expected:
  quota_available: false
```
