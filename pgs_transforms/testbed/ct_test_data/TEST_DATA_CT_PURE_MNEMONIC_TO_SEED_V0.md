# TEST_DATA_CT_PURE_MNEMONIC_TO_SEED_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_MNEMONIC_TO_SEED_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_MNEMONIC_TO_SEED_V0
  description: |
    Test BIP-39 seed derivation from mnemonic phrase via PBKDF2.
  target_artifact: CT_PURE_MNEMONIC_TO_SEED_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_MNEMONIC_TO_SEED_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_MNEMONIC_TO_SEED_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_MNEMONIC_TO_SEED_V0"
```

## Purpose

Test BIP-39 seed derivation from mnemonic phrase via PBKDF2.

## Test Cases

### Case 1: mnemonic_to_seed_basic

**Description:** Derive seed from standard 12-word mnemonic

```yaml
case_id: mnemonic_to_seed_basic
expected_outcome: SUCCESS
bindings:
  mnemonic: "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

expected:
  seed_bytes: "0x5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4"
```
