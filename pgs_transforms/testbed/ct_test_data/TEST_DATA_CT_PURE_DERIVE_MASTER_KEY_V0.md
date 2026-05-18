# TEST_DATA_CT_PURE_DERIVE_MASTER_KEY_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_DERIVE_MASTER_KEY_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_DERIVE_MASTER_KEY_V0
  description: |
    Test BIP-32 master key derivation from seed via HMAC-SHA512.
  target_artifact: CT_PURE_DERIVE_MASTER_KEY_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_DERIVE_MASTER_KEY_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_DERIVE_MASTER_KEY_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_DERIVE_MASTER_KEY_V0"
```

## Purpose

Test BIP-32 master key derivation from seed via HMAC-SHA512.

## Test Cases

### Case 1: derive_master_key_from_seed

**Description:** Derive master private key and chain code from seed

```yaml
case_id: derive_master_key_from_seed
bindings:
  seed_bytes: "0x5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4"

expected:
  master_private_key_bytes: "0x1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67"
  master_chain_code_bytes: "0x7923408dadd3c7b56eed15567707ae5e5dca089de972e07f3b860450e2a3b70e"
```
