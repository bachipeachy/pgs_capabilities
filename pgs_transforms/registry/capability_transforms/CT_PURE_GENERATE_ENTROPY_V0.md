# CT_PURE_GENERATE_ENTROPY_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_GENERATE_ENTROPY_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** OS-provided cryptographically secure random source

---

## Human

### 1. Intent

Generate cryptographically secure entropy bytes of a specified strength.

This transform produces raw entropy suitable as the root input for higher-order cryptographic constructions such as mnemonic generation, seed derivation, or cryptographic key material.

---

### 2. Rationale

All cryptographic key material ultimately depends on high-quality entropy.

In the existing crypto implementation, entropy generation is embedded within mnemonic generation. This atom extracts that responsibility into a single, protocol-governed primitive, enabling explicit audit, reuse, and isolation of entropy generation from downstream derivation logic.

This atom performs **only entropy generation** — nothing more.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_GENERATE_ENTROPY_V0 (full versioned identifier)
- **Operation:** GENERATE_ENTROPY (execution opcode used in molecules)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Generating entropy for:
  - Mnemonic generation
  - Seed derivation
  - Cryptographic key material
- Any context requiring cryptographically secure random bytes

#### 4.2 Invalid Use Cases

- Generating deterministic identifiers
- Deriving mnemonics, keys, or hashes
- Persisting or caching entropy
- Reusing entropy across executions

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | NO | Entropy is non-deterministic by definition |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Uses OS entropy source only |
| Replay Safe | NO | Replay requires captured outputs |

**Note:**  
Non-determinism is explicit and intentional. This atom is pure in the sense of capability isolation, not reproducibility.

---

### 6. Structural Checklist

Author MUST confirm all items before writing YAML:

- [x] Single responsibility (entropy generation only)
- [x] No implicit state
- [x] No domain semantics
- [x] Inputs fully declared
- [x] Outputs fully declared
- [x] Fail-loud on invalid input
- [x] No hidden control flow

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
- `operation` is not `GENERATE_ENTROPY`
- `ct_purity` is not `ct_pure`
- Required input `entropy_bits` is not declared

**Runtime validation MUST fail if:**
- `entropy_bits` is not one of `{128, 160, 192, 224, 256}`
- `entropy_bits` is not an integer
- Entropy generation returns an invalid length or fails

---

### 9. Observability

This atom does NOT emit domain events.

Execution traces MAY record start and end events but MUST NOT record entropy contents.

---

### 10. Security Considerations

- Entropy MUST originate from a cryptographically secure OS source
- Entropy MUST NOT be reused, cached, or persisted
- Entropy MUST NOT be logged or exposed via traces
- Downstream handling is the caller’s responsibility

---

### 11. Common Pitfalls

- Treating entropy as deterministic
- Reusing entropy across multiple derivations
- Persisting entropy in logs or traces
- Assuming mnemonic or key semantics at this level

---

### 12. Minimal Usage Shape

inputs → CT_PURE_GENERATE_ENTROPY_V0 → entropy_bytes

---

## Machine

```yaml
ct_code: CT_PURE_GENERATE_ENTROPY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Generate secure random entropy
  description: Produces cryptographically secure random bytes of a specified bit strength.
  
  inputs:
    entropy_bits:
      type: integer
      required: true
      allowed_values: [128, 160, 192, 224, 256]
      description: "Strength of entropy in bits"

  outputs:
    entropy_bytes:
      type: hex_string
      required: true
      description: "Raw random bytes as hex string with '0x' prefix"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: GENERATE_ENTROPY
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_generate_entropy_v0
    callable: execute
```
