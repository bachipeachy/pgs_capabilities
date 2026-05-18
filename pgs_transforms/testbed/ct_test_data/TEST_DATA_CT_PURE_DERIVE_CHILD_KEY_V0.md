# TEST_DATA_CT_PURE_DERIVE_CHILD_KEY_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_DERIVE_CHILD_KEY_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_DERIVE_CHILD_KEY_V0
  description: |
    Test BIP-32 child key derivation.
  target_artifact: CT_PURE_DERIVE_CHILD_KEY_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_DERIVE_CHILD_KEY_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_DERIVE_CHILD_KEY_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0"
```

## Purpose

Test BIP-32 child key derivation.

## Test Cases

### Case 1: derive_hardened_child

**Description:** Derive hardened child key (index >= 2^31)

```yaml
case_id: derive_hardened_child
bindings:
  parent_private_key_bytes: "0xf79bb0d317b310b261a55a8ab393b4c8a1aba6fa4d08aef379caba502d5d67f9"
  parent_chain_code_bytes: "0x463223aac10fb13f291a1bc76bc26003d98da661cb76df61e750c139826dea8b"
  index: 2147483648

expected:
  child_private_key_bytes: "0x7272904512add56fef94c7b4cfc62bedd0632afbad680f2eb404e95f2d84cbfa"
  child_chain_code_bytes: "0xcb3c17166cc30eb7fdd11993fb7307531372e565cd7c7136cbfa4655622bc2be"
```

### Case 2: derive_normal_child

**Description:** Derive normal child key (index < 2^31)

```yaml
case_id: derive_normal_child
bindings:
  parent_private_key_bytes: "0xf79bb0d317b310b261a55a8ab393b4c8a1aba6fa4d08aef379caba502d5d67f9"
  parent_chain_code_bytes: "0x463223aac10fb13f291a1bc76bc26003d98da661cb76df61e750c139826dea8b"
  index: 0

expected:
  child_private_key_bytes: "0x39f329fedba2a68e2a804fcd9aeea4104ace9080212a52ce8b52c1fb89850c72"
  child_chain_code_bytes: "0x05aae71d7c080474efaab01fa79e96f4c6cfe243237780b0df4bc36106228e31"
```
