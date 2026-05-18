# TEST_DATA_CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
  description: |
    Test Ethereum address derivation from uncompressed public key.
  target_artifact: CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0"
```

## Purpose

Test Ethereum address derivation from uncompressed public key.

## Test Cases

### Case 1: pubkey_to_address

**Description:** Derive Ethereum address from public key

```yaml
case_id: pubkey_to_address
bindings:
  public_key_uncompressed_bytes: "0x04000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f"

expected:
  eth_address_hex: "0x5cd71875c4d0ab1708a380e03fefc3a28aa24831"
```
