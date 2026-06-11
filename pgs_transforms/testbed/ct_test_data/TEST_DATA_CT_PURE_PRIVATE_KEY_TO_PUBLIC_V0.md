# TEST_DATA_CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
  description: |
    Test elliptic curve public key derivation from private key.
  target_artifact: CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0"
```

## Purpose

Test elliptic curve public key derivation from private key.

## Test Cases

### Case 1: secp256k1_pubkey

**Description:** Derive uncompressed public key on secp256k1

```yaml
case_id: secp256k1_pubkey
expected_outcome: SUCCESS
bindings:
  private_key_bytes: "0xf79bb0d317b310b261a55a8ab393b4c8a1aba6fa4d08aef379caba502d5d67f9"
  curve: "secp256k1"

expected:
  public_key_uncompressed_bytes: "0x0452c616d91a2488c1fd1f0f172e98f7d1f6e51f8f389b2f8d632a8b490d5f6da9e31e8d2571464198117614b47ddb7238c7c9d3706c3d05daf937e2c387b49c6e"
```
