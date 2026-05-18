# CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** Elliptic Curve Cryptography (SECP256K1, SECP256R1)

---

## Human

### 1. Intent

Derive an uncompressed public key point from a private scalar on a specified elliptic curve.

This transform performs the scalar multiplication `P = k * G` where `k` is the private key scalar and `G` is the generator point of the specified curve.

---

### 2. Rationale

Public key derivation is the bridge between private key management (HD wallets) and public identity (addresses, verification). This atom isolates the curve mathematics, ensuring explicit curve selection and consistent output formatting (uncompressed).

This atom performs **only EC point multiplication**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
- **Operation:** PRIVATE_KEY_TO_PUBLIC

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Generating a public key from a derived private key
- Preparing a key for address generation
- Verifying keypair consistency

#### 4.2 Invalid Use Cases

- HD derivation (use CT_PURE_DERIVE_CHILD_KEY_V0)
- Address generation (use CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0)
- Signature generation
- Compressed key formatting (compression is a presentation concern)

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same scalar+curve yields same point |
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
- `private_key_bytes` is not valid for the curve (0 or >= order)
- `curve` is not a supported enum value
- `private_key_bytes` length is incorrect for the curve

---

### 9. Observability

This atom does NOT emit domain events.

Key bytes MUST NOT be logged in traces.

---

### 10. Security Considerations

- Private keys are highly sensitive
- Callers must ensure secure handling
- Curve selection must be explicit to prevent cross-curve attacks

---

### 11. Minimal Usage Shape

(private_key_bytes, curve) → CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0 → public_key_uncompressed_bytes

---

## Machine

```yaml
ct_code: CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Derive public key from private scalar
  description: Performs elliptic curve scalar multiplication (P = k * G) to derive an uncompressed public key.
  
  inputs:
    private_key_bytes:
      type: hex_string
      required: true
      description: "Private key scalar as hex string with '0x' prefix"
    curve:
      type: string
      required: true
      enum: ["secp256k1", "secp256r1"]
      description: "The elliptic curve to use for derivation."

  outputs:
    public_key_uncompressed_bytes:
      type: hex_string
      required: true
      description: "Uncompressed public key point (0x04 || X || Y) as hex string with '0x' prefix"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: PRIVATE_KEY_TO_PUBLIC
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_private_key_to_public_v0
    callable: execute
```
