# CT_PURE_MNEMONIC_TO_SEED_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_MNEMONIC_TO_SEED_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** BIP-39 PBKDF2 seed derivation rules

---

## Human

### 1. Intent

Derive a cryptographic seed from a BIP-39 mnemonic phrase.

This transform applies the standardized PBKDF2 function to produce
a deterministic seed suitable for hierarchical key derivation.

---

### 2. Rationale

Seed derivation must be deterministic, standardized, and cryptographically
sound. This atom isolates mnemonic-to-seed derivation so that it may be reused
independently of wallet or ledger semantics.

This atom performs **only mnemonic-to-seed derivation**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_MNEMONIC_TO_SEED_V0
- **Operation:** MNEMONIC_TO_SEED

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Wallet seed derivation
- Key hierarchy initialization
- Deterministic wallet recovery

#### 4.2 Invalid Use Cases

- Entropy generation
- Key derivation beyond seed production
- Domain-specific wallet/ledger policy

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same mnemonic yields same seed |
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
- MAY be composed by molecules

---

### 8. Validation Expectations

**Runtime validation MUST fail if:**
- `mnemonic` is not a string
- Seed derivation fails

---

### 9. Observability

This atom does NOT emit domain events.

Seed bytes MUST NOT be logged in traces.

---

### 10. Security Considerations

- Mnemonics and seeds are highly sensitive
- Callers must ensure secure handling

---

### 11. Minimal Usage Shape

mnemonic → CT_PURE_MNEMONIC_TO_SEED_V0 → seed_bytes

---

## Machine

```yaml
ct_code: CT_PURE_MNEMONIC_TO_SEED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Derive seed from BIP-39 mnemonic
  description: Applies BIP-39 seed derivation (PBKDF2) to a mnemonic phrase.
  
  inputs:
    mnemonic:
      type: string
      required: true
      description: "BIP-39 mnemonic phrase"

  outputs:
    seed_bytes:
      type: hex_string
      required: true
      description: "Derived deterministic seed as hex string with '0x' prefix"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: MNEMONIC_TO_SEED
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_mnemonic_to_seed_v0
    callable: execute
```
