# CT_PURE_DERIVE_CHILD_KEY_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_DERIVE_CHILD_KEY_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** BIP-32 child key derivation rules

---

## Human

### 1. Intent

Derive a single BIP-32 child private key and chain code from a parent key.

This transform applies the standardized CKDpriv function to produce
a deterministic child key at a specific index.

This atom implements the Bitcoin BIP-32 child key derivation. It supports both hardened (index >= 2^31) and non-hardened derivation.

---

### 2. Rationale

Child key derivation is the fundamental operation for traversing HD wallet trees.
This atom isolates the single-step derivation logic, ensuring it is stateless
and agnostic to the overall derivation path or wallet structure.

This atom performs **only single-step child derivation**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_DERIVE_CHILD_KEY_V0
- **Operation:** DERIVE_CHILD_KEY

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Deriving a specific child key from a parent
- Traversing one level of an HD path
- Address generation at a specific index

#### 4.2 Invalid Use Cases

- Master key generation
- Multi-step path derivation (use a molecule)
- Public key derivation (use CT_PRIVATE_KEY_TO_PUBLIC_V0)

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same parent+index yields same child |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure cryptographic transform |
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
- MAY be composed by molecules (e.g., for path derivation)

---

### 8. Validation Expectations

**Runtime validation MUST fail if:**
- `parent_private_key_bytes` is not 32 bytes
- `parent_chain_code_bytes` is not 32 bytes
- `index` is not a 32-bit integer
- Derived key is invalid (0 or >= curve order)

---

### 9. Observability

This atom does NOT emit domain events.

Key bytes MUST NOT be logged in traces.

---

### 10. Security Considerations

- Private keys are highly sensitive
- Callers must ensure secure handling
- Hardened derivation (index >= 0x80000000) is recommended for security

---

### 11. Minimal Usage Shape

(parent_private_key_bytes, parent_chain_code_bytes, index) → CT_PURE_DERIVE_CHILD_KEY_V0 → (child_private_key_bytes, child_chain_code_bytes)

---

## Machine

```yaml
ct_code: CT_PURE_DERIVE_CHILD_KEY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Derive BIP-32 child key
  description: Implements BIP-32 CKDpriv function to derive child private key and chain code from parent.
  
  inputs:
    parent_private_key_bytes:
      type: hex_string
      required: true
      description: "32-byte parent private key as hex string with '0x' prefix"
    parent_chain_code_bytes:
      type: hex_string
      required: true
      description: "32-byte parent chain code as hex string with '0x' prefix"
    index:
      type: integer
      required: true
      description: "32-bit index. Values >= 2147483648 (0x80000000) denote hardened derivation."

  outputs:
    child_private_key_bytes:
      type: hex_string
      required: true
      description: "32-byte derived child private key as hex string with '0x' prefix"
    child_chain_code_bytes:
      type: hex_string
      required: true
      description: "32-byte derived child chain code as hex string with '0x' prefix"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: DERIVE_CHILD_KEY
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_derive_child_key_v0
    callable: execute
```
