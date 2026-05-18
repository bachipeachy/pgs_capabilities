# TEST_DATA_CT_PURE_CHECK_TRAINING_STATUS_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_CHECK_TRAINING_STATUS_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_CHECK_TRAINING_STATUS_V0
  description: |
    Test training completion eligibility check.
  target_artifact: CT_PURE_CHECK_TRAINING_STATUS_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_CHECK_TRAINING_STATUS_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_CHECK_TRAINING_STATUS_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_CHECK_TRAINING_STATUS_V0"
```

## Purpose

Test training completion eligibility check.

## Test Cases

### Case 1: training_completed

**Description:** Training is completed, user is eligible

```yaml
case_id: training_completed
bindings:
  training_completed: true

expected:
  is_eligible: true
```

### Case 2: training_not_completed

**Description:** Training not completed, user is ineligible

```yaml
case_id: training_not_completed
bindings:
  training_completed: false

expected:
  is_eligible: false
```
