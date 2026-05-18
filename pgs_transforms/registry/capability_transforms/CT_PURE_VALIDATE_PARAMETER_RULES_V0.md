# CT_PURE_VALIDATE_PARAMETER_RULES_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_VALIDATE_PARAMETER_RULES_V0
- **Artifact Kind:** capability_transform
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Evaluate declarative parameter constraint rules against a parameter map.

---

## 2. Rationale

Parameter rule validation is a generic governance primitive:
- Rules are declared in governance artifacts, not in code
- Supports operators: eq, neq, lte, gte, lt, gt, in, not_null
- Domain-agnostic — any parameter map can be validated against any rule set

---

## 3. Purity

| Property | Value |
|----------|-------|
| Purity | ct_pure |
| Kind | atom |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| parameters | object | true | Parameter key-value map to validate |
| rules | array | true | Array of rule objects with field, op, and value/allowed |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| valid | boolean | Whether all rules passed |
| failed_rule | object | First failed rule object (null if all passed) |

---

## 6. Result Status

| Status | Condition |
|--------|-----------|
| SUCCESS | All rules pass (valid=true) |
| VIOLATION | First failed rule (valid=false, failed_rule populated) |

---

## Machine

```yaml
ct_code: CT_PURE_VALIDATE_PARAMETER_RULES_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Validate parameters against rules
  description: Evaluates a set of declarative constraint rules (eq, gt, in, etc.) against a provided parameter map.
  
  inputs:
    parameters:
      type: object
      required: true
      description: Parameter key-value map to validate
    rules:
      type: array
      required: true
      description: List of constraint rule objects

  outputs:
    valid:
      type: boolean
      required: true
      description: True if all rules passed
    failed_rule:
      type: object
      required: false
      nullable: true
      description: The first rule that failed validation (null if all pass)

machine:
  ct_kind: atom
  ct_purity: ct_pure
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_validate_parameter_rules_v0
    callable: execute
```
