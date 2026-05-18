# CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
- **Artifact Kind:** capability_transform
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Validate that a value is a member of a declared set.

---

## 2. Rationale

Set membership validation is a generic governance primitive:
- Checks whether a value appears in a declared allowed set
- Used for closed-registry enforcement, status validation, tool surface checks
- Domain-agnostic — the set is provided as input, not hardcoded

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
| value | string | true | Value to check for membership |
| allowed_set | array | true | Set of allowed values |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| is_member | boolean | Whether value is in allowed_set |

---

## 6. Result Status

| Status | Condition |
|--------|-----------|
| SUCCESS | Value is a member of allowed_set (is_member=true) |
| VIOLATION | Value is not a member of allowed_set |

---

## Machine

```yaml
ct_code: CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Validate set membership
  description: Checks whether a specific value exists within a provided array of allowed values.
  
  inputs:
    value:
      type: string
      required: true
      description: The value to check
    allowed_set:
      type: array
      required: true
      description: The list of permitted values

  outputs:
    is_member:
      type: boolean
      required: true
      description: True if value is found in allowed_set

machine:
  ct_kind: atom
  ct_purity: ct_pure
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_validate_set_membership_v0
    callable: execute
```
