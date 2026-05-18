# CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** Keccak-256 (SHA-3)

---

## Human

### 1. Intent

Derive an Ethereum address from an uncompressed public key.

This transform applies the standard Ethereum address derivation algorithm:
1. Drop the first byte (0x04 prefix) from the uncompressed public key.
2. Compute the Keccak-256 hash of the remaining 64 bytes.
3. Take the last 20 bytes of the hash as the address.

---

### 2. Rationale

Address derivation is the final step in identity creation. This atom isolates the Ethereum-specific address format logic from key derivation. It is strictly a formatting and hashing operation, with no curve mathematics involved.

This atom performs **only public-key-to-address derivation**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
- **Operation:** PUBKEY_TO_ETH_ADDRESS

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Generating an Ethereum address from a public key
- Verifying address ownership (given a public key)

#### 4.2 Invalid Use Cases

- Key derivation (use CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0)
- Checksum formatting (EIP-55 is a presentation concern, use a separate atom or molecule if needed)
- Chain-specific logic (this atom is chain-agnostic)

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same public key yields same address |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure hashing transform |
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
- `public_key_uncompressed_bytes` is not 65 bytes
- `public_key_uncompressed_bytes` does not start with 0x04

---

### 9. Observability

This atom does NOT emit domain events.

Address bytes MAY be logged (they are public identifiers), but PII rules apply.

---

### 10. Security Considerations

- Ensure the input is a valid uncompressed public key
- This atom does not validate the mathematical validity of the point, only its format

---

### 11. Minimal Usage Shape

public_key_uncompressed_bytes → CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0 → eth_address_hex

---

## Machine

```yaml
ct_code: CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Derive ETH address from public key
  description: Applies the Ethereum address derivation algorithm (Keccak-256 hash of public key, last 20 bytes).
  
  inputs:
    public_key_uncompressed_bytes:
      type: hex_string
      required: true
      description: "Uncompressed public key (65 bytes, starting with 0x04) as hex string with '0x' prefix"

  outputs:
    eth_address_hex:
      type: string
      required: true
      description: "Ethereum address as a 0x-prefixed hex string (42 characters)"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: PUBKEY_TO_ETH_ADDRESS
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_pubkey_to_eth_address_v0
    callable: execute
```
