# CT_PURE_DERIVE_MASTER_KEY_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_DERIVE_MASTER_KEY_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** BIP-32 master key derivation rules

---

## Human

### 1. Intent

Derive a BIP-32 master private key and chain code from a seed.

This transform applies the standardized HMAC-SHA512 function to produce
a deterministic master key and chain code suitable for hierarchical key derivation.

This atom implements the Bitcoin BIP-32 master key derivation using HMAC-SHA512 with the standard “Bitcoin seed” key. Curve application occurs in downstream atoms.

---

### 2. Rationale

Master key derivation must be deterministic, standardized, and cryptographically
sound. This atom isolates seed-to-master-key derivation so that it may be reused
independently of wallet or ledger semantics.

This atom performs **only seed-to-master-key derivation**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_DERIVE_MASTER_KEY_V0
- **Operation:** DERIVE_MASTER_KEY

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Wallet master key initialization
- Key hierarchy root derivation
- Deterministic wallet recovery

#### 4.2 Invalid Use Cases

- Entropy generation
- Mnemonic handling
- Child key derivation
- Domain-specific wallet/ledger policy

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same seed yields same master key |
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
- `seed_bytes` is not bytes
- `seed_bytes` length < 128 bits
- Derived key is invalid (0 or >= curve order)

---

### 9. Observability

This atom does NOT emit domain events.

Key bytes MUST NOT be logged in traces.

---

### 10. Security Considerations

- Seeds and private keys are highly sensitive
- Callers must ensure secure handling

---

### 11. Minimal Usage Shape

seed_bytes → CT_PURE_DERIVE_MASTER_KEY_V0 → (master_private_key_bytes, master_chain_code_bytes)

---

## Machine

```yaml
ct_code: CT_PURE_DERIVE_MASTER_KEY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Derive BIP-32 master key from seed
  description: Applies HMAC-SHA512 to a seed to derive a deterministic BIP-32 master private key and chain code.
  
  inputs:
    seed_bytes:
      type: hex_string
      required: true
      description: "Seed bytes as hex string with '0x' prefix (e.g., from mnemonic) at least 128 bits long"

  outputs:
    master_private_key_bytes:
      type: hex_string
      required: true
      description: "32-byte derived master private key as hex string"
    master_chain_code_bytes:
      type: hex_string
      required: true
      description: "32-byte derived master chain code as hex string"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: DERIVE_MASTER_KEY
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_derive_master_key_v0
    callable: execute
```
