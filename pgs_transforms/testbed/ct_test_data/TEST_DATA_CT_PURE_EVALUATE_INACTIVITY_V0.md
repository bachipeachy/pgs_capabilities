# TEST_DATA_CT_PURE_EVALUATE_INACTIVITY_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_EVALUATE_INACTIVITY_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_EVALUATE_INACTIVITY_V0
  description: |
    Test inactivity evaluation based on date thresholds.
  target_artifact: CT_PURE_EVALUATE_INACTIVITY_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_EVALUATE_INACTIVITY_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_EVALUATE_INACTIVITY_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_EVALUATE_INACTIVITY_V0"
```

## Purpose

Test inactivity evaluation based on date thresholds.

## Test Cases

### Case 1: user_inactive

**Description:** User inactive beyond threshold

```yaml
case_id: user_inactive
expected_outcome: SUCCESS
bindings:
  last_active_date: "2024-01-01T00:00:00Z"
  threshold_days: 30
  current_date: "2024-02-15T00:00:00Z"

expected:
  is_inactive: true
  days_inactive: 45
```

### Case 2: user_active

**Description:** User active within threshold

```yaml
case_id: user_active
expected_outcome: SUCCESS
bindings:
  last_active_date: "2024-02-10T00:00:00Z"
  threshold_days: 30
  current_date: "2024-02-15T00:00:00Z"

expected:
  is_inactive: false
  days_inactive: 5
```
