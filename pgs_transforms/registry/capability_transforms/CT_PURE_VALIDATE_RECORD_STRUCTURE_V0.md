# CT_PURE_VALIDATE_RECORD_STRUCTURE_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Validate a record against a provided schema of field validation rules.

This transform accepts an arbitrary record (object) and a schema describing
expected field types, patterns, and constraints. It returns a result status
and a list of violations.

---

### 2. Rationale

Record validation is a generic infrastructure concern. The schema is
supplied by the caller (typically a capability contract), keeping
this atom domain-neutral. No domain words appear in this atom.

This atom performs **only structural record validation**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
- **Operation:** VALIDATE_RECORD_STRUCTURE

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Validating field types and formats
- Checking required field presence
- Pattern matching on string fields
- Range and length constraints

#### 4.2 Invalid Use Cases

- Domain-specific business rules (use a domain CC)
- Cross-record validation (use a domain CC)
- Schema inference or discovery

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same record + schema yields same result |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure validation transform |
| Replay Safe | YES | Deterministic mapping |

---

### 6. Structural Checklist

- [x] Single responsibility
- [x] Deterministic
- [x] No implicit state
- [x] Inputs fully declared
- [x] Outputs fully declared
- [x] Fail-loud on invalid input

---

### 7. Composition Rules

As an **atom**, this CT:
- MUST NOT invoke other CTs
- MUST perform exactly one transformation
- MAY be composed by molecules

---

### 8. Validation Expectations

**Runtime validation MUST fail if:**
- `record` is not an object
- `schema` is not an object

---

### 9. Observability

 This atom does NOT emit domain events.

Validation results MAY be logged for diagnostics.

---

### 10. Security Considerations

- Schema patterns use regex — callers must not pass untrusted patterns
- No secret material is involved in validation

---

### 11. Minimal Usage Shape

{record, schema} → CT_PURE_VALIDATE_RECORD_STRUCTURE_V0 → {violations}

---

## Machine

```yaml
ct_code: CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Validate record structure
  description: Validates an arbitrary record object against a provided schema of field rules (type, pattern, required, etc.).
  
  inputs:
    record:
      type: object
      required: true
      description: "The record to validate"
    schema:
      type: object
      required: true
      description: "Validation rules keyed by field name"

  outputs:
    violations:
      type: array
      required: true
      description: "List of violation objects with field, rule, and message"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: VALIDATE_RECORD_STRUCTURE
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_validate_record_structure_v0
    callable: execute
```
