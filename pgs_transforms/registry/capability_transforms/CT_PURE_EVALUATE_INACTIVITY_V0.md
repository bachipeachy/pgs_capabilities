# CT_PURE_EVALUATE_INACTIVITY_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_EVALUATE_INACTIVITY_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Evaluate whether a license holder has been inactive beyond a threshold.

This transform compares last active date against a threshold and returns inactivity status.

---

### 2. Rationale

Inactivity evaluation enables autonomous license reclamation.

This transform provides:
- Deterministic inactivity check
- Domain-agnostic date comparison
- Threshold-based evaluation

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_EVALUATE_INACTIVITY_V0 (full versioned identifier)
- **Operation:** EVALUATE_INACTIVITY (execution opcode)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases
- Evaluating license holder inactivity
- Gating reclamation workflows
- Computing days since last activity

#### 4.2 Invalid Use Cases
- Modifying activity records
- Querying external usage systems
- Implementing complex reclamation policies

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same inputs yield same output |
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
- Required inputs (`last_active_date`, `threshold_days`, `current_date`) are not declared
- Outputs (`is_inactive`, `days_inactive`) are not declared

**Runtime validation MUST fail if:**
- Date inputs are not valid ISO 8601 strings
- Threshold is negative
- Implementation raises an exception

---

### 9. Observability

This atom does NOT emit traces.

**Rationale:** Pure computation with no side effects or state changes.

---

### 10. Common Pitfalls

- Using system clock instead of explicit current_date input (violates determinism)
- Encoding reclamation policies (violates single responsibility)
- Performing side effects on usage records (violates purity)

---

### 11. Minimal Usage Shape

```
(last_active_date, threshold_days, current_date) → CT_PURE_EVALUATE_INACTIVITY_V0 → (is_inactive, days_inactive)
```

---

## Machine

```yaml
ct_code: CT_PURE_EVALUATE_INACTIVITY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Evaluate inactivity threshold
  description: Compares a last active date against a threshold relative to current date to determine inactivity status.
  
  inputs:
    last_active_date:
      type: string
      format: date-time
      required: true
      description: ISO 8601 timestamp of last activity
    threshold_days:
      type: integer
      required: true
      description: Number of days before considering a holder inactive
    current_date:
      type: string
      format: date-time
      required: true
      description: ISO 8601 timestamp of current evaluation time

  outputs:
    is_inactive:
      type: boolean
      required: true
      description: True if inactive beyond threshold
    days_inactive:
      type: integer
      required: true
      description: Total days since last activity

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: EVALUATE_INACTIVITY
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_evaluate_inactivity_v0
    callable: execute
```
