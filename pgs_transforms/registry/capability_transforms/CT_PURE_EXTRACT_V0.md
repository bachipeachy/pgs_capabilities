# CT_PURE_EXTRACT_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_EXTRACT_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Extract a value from an execution context using a declarative JSONPath expression.

This transform maps a structured input context and a path selector to a single extracted output value.

---

### 2. Rationale

Many transformation pipelines require selective access to nested or structured data without embedding traversal logic in higher-level artifacts.

This transform provides:
- Reusable, deterministic value extraction
- Independence from domain semantics
- Separation from execution flow
- Protocol-governed data access patterns

Without a canonical extraction mechanism, field access would be implicit, engine-specific, or scattered across multiple atoms.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_EXTRACT_V0 (full versioned identifier)
- **Operation:** EXTRACT (execution opcode used in molecules)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases
- Extracting a specific value from structured input data
- Normalizing access to deeply nested structures
- Preparing inputs for downstream CTs
- Selecting fields from prior step results

#### 4.2 Invalid Use Cases
- Performing conditional logic based on extracted values
- Encoding domain meaning into path expressions
- Mutating or restructuring the source context
- Implementing data transformation (use dedicated transform atoms)

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same input and path yield same output |
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
- `operation` is not `EXTRACT`
- `ct_purity` is not `ct_pure`
- Required inputs (`from`, `path`, `type`) are not declared
- Output `result` is not declared

**Runtime validation MUST fail if:**
- JSONPath expression in `path` is invalid
- Symbol referenced in `from` does not exist
- Extracted value cannot be coerced to declared `type`
- Path resolves to undefined or null (unless explicitly permitted)
- Implementation raises an exception

---

### 9. Observability

This atom does NOT emit traces.

**Rationale:** Pure computation with no side effects or state changes.

---

### 10. Common Pitfalls

- Treating `path` as a domain contract rather than a structural selector (violates semantic blindness)
- Encoding conditional logic into path expressions (use dedicated branching atoms)
- Assuming presence of fields without validation (causes runtime failures)
- Using EXTRACT to reshape data instead of selecting it (violates single responsibility)
- Mixing JSONPath with domain-specific query languages

---

### 11. Minimal Usage Shape

```
context → CT_PURE_EXTRACT_V0 → value
```

**Example in molecule context:**
```
step_1: GENERATE_ID → id_result
step_2: EXTRACT(from=id_result, path=$.id) → extracted_id
```

---

## Machine

```yaml
ct_code: CT_PURE_EXTRACT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Extract a value using JSONPath
  description: Extracts a single value from a structured context or object using a declarative JSONPath expression.
  
  inputs:
    from:
      type: any
      required: true
      description: Context symbol or object to extract from
    path:
      type: string
      required: true
      description: JSONPath expression selector
    type:
      type: string
      required: true
      description: Expected output type for validation

  outputs:
    result:
      type: any
      description: The extracted value

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: EXTRACT
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_extract_v0
    callable: execute
```
