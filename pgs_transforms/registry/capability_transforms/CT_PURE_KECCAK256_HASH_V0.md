# CT_PURE_KECCAK256_HASH_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_KECCAK256_HASH_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** Keccak-256 (pycryptodome)

---

## Machine

```yaml
ct_code: CT_PURE_KECCAK256_HASH_V0
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Compute Keccak-256 hash
  description: Returns the Keccak-256 (SHA-3 variant) cryptographic digest of input bytes.
  
  inputs:
    input_bytes:
      type: string
      required: true
      description: "Hex-encoded byte string (with or without 0x prefix)"

  outputs:
    hash_hex:
      type: string
      required: true
      description: "Keccak-256 hash as 0x-prefixed hex string (66 characters)"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: KECCAK256_HASH
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_keccak256_hash_v0
    callable: execute
```
