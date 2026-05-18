# CT_PURE_CHECK_QUOTA_AVAILABLE_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_CHECK_QUOTA_AVAILABLE_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Check whether quota capacity is available (assigned count is less than quota limit).

This transform compares two integers and returns availability status.

---

### 2. Rationale

Quota enforcement is a hard limit in bounded-capacity workflows.

This transform provides:
- Deterministic capacity check
- Domain-agnostic integer comparison
- Count-based enforcement (not currency)
- Reusable across licenses, seats, wallets, entitlements, limits

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_CHECK_QUOTA_AVAILABLE_V0 (full versioned identifier)
- **Operation:** CHECK_QUOTA_AVAILABLE (execution opcode)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases
- Evaluating license quota before provisioning
- Evaluating seat capacity before assignment
- Evaluating entitlement limits
- Gating workflows when quota is exhausted
- Composing with other eligibility checks

#### 4.2 Invalid Use Cases
- Modifying quota or count values
- Querying external systems
- Implementing complex allocation logic
- Domain-specific quota policies

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
- Required inputs (`assigned_count`, `quota`) are not declared
- Output `quota_available` is not declared

**Runtime validation MUST fail if:**
- Inputs are not integers
- Quota is negative
- Implementation raises an exception

---

### 9. Observability

This atom does NOT emit traces.

**Rationale:** Pure computation with no side effects or state changes.

---

### 10. Common Pitfalls

- Encoding allocation strategies (violates single responsibility)
- Performing side effects on count (violates purity)
- Returning non-boolean values
- Embedding domain semantics (use domain binding instead)

---

### 11. Minimal Usage Shape

```
(assigned_count, quota) → CT_PURE_CHECK_QUOTA_AVAILABLE_V0 → quota_available
```

**Domain binding example:**
```
In ai_licensing: quota = license_cap
In seats_mgmt:   quota = seat_limit
In entitlements: quota = max_entitlements
```

---

## Machine

```yaml
ct_code: CT_PURE_CHECK_QUOTA_AVAILABLE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Check quota capacity availability
  description: Compares current assigned count against a quota limit to determine if capacity remains.
  
  inputs:
    assigned_count:
      type: integer
      required: true
      description: Current count of assigned items
    quota:
      type: integer
      required: true
      description: Maximum allowed count (quota)

  outputs:
    quota_available:
      type: boolean
      required: true
      description: True if assigned_count is less than quota

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: CHECK_QUOTA_AVAILABLE
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_check_quota_available_v0
    callable: execute
```
