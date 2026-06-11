# TEST_DATA_CT_PURE_ECDSA_SIGN_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_ECDSA_SIGN_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_ECDSA_SIGN_V0
  description: |
    Test ECDSA signature generation.
  target_artifact: CT_PURE_ECDSA_SIGN_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_ECDSA_SIGN_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_ECDSA_SIGN_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_ECDSA_SIGN_V0"
```

## Purpose

Test ECDSA signature generation.

## Test Cases

### Case 1: sign_message_secp256k1

**Description:** Sign message hash with secp256k1

```yaml
case_id: sign_message_secp256k1
expected_outcome: SUCCESS
bindings:
  private_key_bytes: "0xf79bb0d317b310b261a55a8ab393b4c8a1aba6fa4d08aef379caba502d5d67f9"
  message_hash: "0xb94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
  curve: "secp256k1"

expected:
  v: 0
  r: "0x2376b8cb03c29e7df673eb0ef4713e0f767aa016564a404339da276ab42e78cf"
  s: "0x7f5c4d7cd2c32ab8ca1a5f411857ed7d52a1edd3003bc334272bb3f4fdbaac37"
  signed_bytes: "0x2376b8cb03c29e7df673eb0ef4713e0f767aa016564a404339da276ab42e78cf7f5c4d7cd2c32ab8ca1a5f411857ed7d52a1edd3003bc334272bb3f4fdbaac3700"
```
