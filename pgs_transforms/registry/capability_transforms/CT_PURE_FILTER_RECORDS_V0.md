# CT_PURE_FILTER_RECORDS_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_FILTER_RECORDS_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Filter an array of record objects by declared field criteria, returning only those records that satisfy all criteria.

---

### 2. Rationale

Many pipeline stages require selecting a subset of records from a list based on field conditions (exact-value match or field presence). This transform provides a reusable, declarative, domain-agnostic filtering primitive for use in CC pipelines that operate on arrays returned from CS store operations.

Without a canonical filter atom, filtering logic would be duplicated or embedded ad hoc in domain-specific transforms.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_FILTER_RECORDS_V0 (full versioned identifier)
- **Operation:** FILTER_RECORDS (execution opcode used in molecules)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases
- Filtering a CS store LIST result to eligible records by field conditions
- Selecting records by exact field value or field presence
- Preparing a filtered list for downstream CC steps

#### 4.2 Invalid Use Cases
- Filtering by complex expressions, ranges, or nested conditions
- Sorting or ordering records
- Reshaping or transforming record fields
- Domain-specific eligibility logic (that belongs in domain CC)

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same source and filter yield same output |
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

### 8. Filter Criterion Semantics

The `filter` input is a flat dict of field criteria applied with AND logic:

| Criterion Value | Semantic |
|----------------|---------|
| `"present"` | Field must exist in record and not be None |
| any other value | Field must equal that value exactly |

All criteria must be satisfied for a record to be included.

---

### 9. Validation Expectations

**Runtime validation MUST fail if:**
- `source` is not an array
- `filter` is not an object
- No records satisfy all filter criteria (raises CTExecutionError → VIOLATION at CC)

---

### 10. Observability

This atom does NOT emit traces.

**Rationale:** Pure computation with no side effects or state changes.

---

## Machine

```yaml
ct_code: CT_PURE_FILTER_RECORDS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Filter an array of records by declared field criteria
  description: Accepts a source array and a filter criteria object. Returns only records satisfying all criteria. Raises CTExecutionError if no records match.

  inputs:
    source:
      type: array
      required: true
      description: Array of record objects to filter
    filter:
      type: object
      required: true
      description: Field criteria dict. Values are exact match or "present" for existence check.

  outputs:
    extracted:
      type: array
      description: Filtered records satisfying all criteria

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: FILTER_RECORDS
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_filter_records_v0
    callable: execute
```