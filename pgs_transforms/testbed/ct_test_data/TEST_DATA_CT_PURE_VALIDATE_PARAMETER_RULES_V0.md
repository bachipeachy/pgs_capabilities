# TEST_DATA_CT_PURE_VALIDATE_PARAMETER_RULES_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_VALIDATE_PARAMETER_RULES_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_VALIDATE_PARAMETER_RULES_V0
  description: |
    Test parameter validation against rules.
  target_artifact: CT_PURE_VALIDATE_PARAMETER_RULES_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_VALIDATE_PARAMETER_RULES_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_VALIDATE_PARAMETER_RULES_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0"
```

## Purpose

Test parameter validation against rules.

## Test Cases

### Case 1: all_rules_pass

**Description:** All validation rules pass

```yaml
case_id: all_rules_pass
bindings:
  parameters:
    amount: 100
    type: "deposit"
  rules:
    - field: "amount"
      op: "gt"
      value: 0

expected:
  valid: true
  failed_rule: null
```

### Case 2: rule_fails

**Description:** One validation rule fails

```yaml
case_id: rule_fails
bindings:
  parameters:
    amount: -50
    type: "deposit"
  rules:
    - field: "amount"
      op: "gt"
      value: 0

expected:
  valid: false
  failed_rule:
    field: "amount"
    op: "gt"
    value: 0
```
