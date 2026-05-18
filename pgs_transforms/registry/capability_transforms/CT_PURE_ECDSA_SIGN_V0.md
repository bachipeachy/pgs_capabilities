# CT_PURE_ECDSA_SIGN_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_ECDSA_SIGN_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** coincurve (secp256k1)

---

## Human

### 1. Intent

Sign a message hash using ECDSA with a specified elliptic curve.

This transform accepts a 32-byte private key and a 32-byte message hash,
produces a recoverable ECDSA signature with (v, r, s) components.

---

### 2. Rationale

ECDSA signing is a fundamental cryptographic primitive used in Ethereum
for transaction authorization. This atom isolates the signing operation
from key derivation, transaction encoding, and domain logic.

This atom performs **only ECDSA signing**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_ECDSA_SIGN_V0
- **Operation:** ECDSA_SIGN

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Transaction signing
- Message signing
- Any ECDSA signature operation on secp256k1

#### 4.2 Invalid Use Cases

- Key generation or derivation
- Signature verification
- Non-ECDSA signature schemes (EdDSA, Schnorr)

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same key + hash yields same signature (RFC 6979) |
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
- `private_key_bytes` is not 32 bytes
- `message_hash` is not 32 bytes
- `curve` is not a supported curve
- Signing fails

---

### 9. Observability

This atom does NOT emit domain events.

Private keys and signatures MUST NOT be logged in traces.

---

### 10. Security Considerations

- Private key material is highly sensitive
- Callers must ensure secure handling and immediate disposal
- Only the (v, r, s) components should be persisted, never the private key

---

### 11. Minimal Usage Shape

private_key_bytes + message_hash → CT_PURE_ECDSA_SIGN_V0 → {v, r, s, signed_bytes}

---

## Machine

```yaml
ct_code: CT_PURE_ECDSA_SIGN_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Sign message hash via ECDSA
  description: Produces a recoverable ECDSA signature (v, r, s) from a private key and message hash.
  
  inputs:
    private_key_bytes:
      type: hex_string
      required: true
      description: "32-byte ECDSA private key as hex string with '0x' prefix"
    message_hash:
      type: hex_string
      required: true
      description: "32-byte message hash to sign as hex string with '0x' prefix"
    curve:
      type: string
      required: false
      default: "secp256k1"
      description: "Elliptic curve to use for signing"

  outputs:
    v:
      type: integer
      description: "Recovery identifier"
    r:
      type: string
      description: "Signature r component as 0x-prefixed hex"
    s:
      type: string
      description: "Signature s component as 0x-prefixed hex"
    signed_bytes:
      type: string
      description: "Full recoverable signature as 0x-prefixed hex (65 bytes)"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: ECDSA_SIGN
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_ecdsa_sign_v0
    callable: execute
```
