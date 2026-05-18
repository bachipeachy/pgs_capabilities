# CT_PURE_CHECK_TRAINING_STATUS_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_CHECK_TRAINING_STATUS_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Check whether an employee has completed required training.

This transform evaluates a boolean flag and returns eligibility status.

---

### 2. Rationale

Training completion is a protocol gate for license provisioning.

This transform provides:
- Deterministic eligibility check
- Domain-agnostic boolean evaluation
- Reusable across any training-gated workflow

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_CHECK_TRAINING_STATUS_V0 (full versioned identifier)
- **Operation:** CHECK_TRAINING_STATUS (execution opcode)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases
- Evaluating training completion flag
- Gating provisioning workflows
- Composing with other eligibility checks

#### 4.2 Invalid Use Cases
- Querying external training systems
- Determining training requirements
- Modifying training status

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same input yields same output |
| Purity Class | ct_pure | No side effects, no state |
| Side Effects | NONE | Fully pure computation |
| Replay Safe | YES | Identical inputs produce identical output |

---

### 6. Structural Checklist

Author MUST confirm all items before writing YAML:

- [x] Single responsibility
- [x] No implicit state
- [x] No domain semantics
- [x] Inputs fully declared
- [x] Outputs fully declared
- [x] No hidden control flow
- [x] Composition rules respected

---

### 7. Composition Rules (Atom-Specific)

As an **atom**, this CT:
- MUST NOT invoke other CTs (atoms or molecules)
- MUST perform exactly one atomic operation
- MAY be composed by molecules

---

### 8. Validation Expectations

**Static validation MUST fail if:**
- `ct_kind` is not `atom`
- `ct_purity` is not `ct_pure`
- Required input (`training_completed`) is not declared
- Output `is_eligible` is not declared

**Runtime validation MUST fail if:**
- Input `training_completed` is not a boolean
- Implementation raises an exception

---

### 9. Observability

This atom does NOT emit traces.

**Rationale:** Pure computation with no side effects or state changes.

---

### 10. Common Pitfalls

- Encoding training-specific business rules (violates domain agnosticism)
- Performing external lookups (violates purity)
- Returning non-boolean values

---

### 11. Minimal Usage Shape

```
training_completed → CT_PURE_CHECK_TRAINING_STATUS_V0 → is_eligible
```

---

## Machine

```yaml
ct_code: CT_PURE_CHECK_TRAINING_STATUS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Check training completion status
  description: Evaluates a boolean flag to determine if training requirements have been met.
  
  inputs:
    training_completed:
      type: boolean
      required: true
      description: "True if training is finished"

  outputs:
    is_eligible:
      type: boolean
      required: true
      description: "True if training_completed is true"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: CHECK_TRAINING_STATUS
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_check_training_status_v0
    callable: execute
```
