# TEST_DATA_CT_PURE_KECCAK256_HASH_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_KECCAK256_HASH_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_KECCAK256_HASH_V0
  description: |
    Test Keccak-256 cryptographic hash computation.
  target_artifact: CT_PURE_KECCAK256_HASH_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_KECCAK256_HASH_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_KECCAK256_HASH_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_KECCAK256_HASH_V0"
```

## Purpose

Test Keccak-256 cryptographic hash computation.

## Test Cases

### Case 1: hash_simple_hex

**Description:** Hash a simple hex string

```yaml
case_id: hash_simple_hex
bindings:
  input_bytes: "0x48656c6c6f"

expected:
  hash_hex: "0x06b3dfaec148fb1bb2b066f10ec285e7c9bf402ab32aa78a5d38e34566810cd2"
```

### Case 2: hash_without_prefix

**Description:** Hash hex string without 0x prefix

```yaml
case_id: hash_without_prefix
bindings:
  input_bytes: "48656c6c6f"

expected:
  hash_hex: "0x06b3dfaec148fb1bb2b066f10ec285e7c9bf402ab32aa78a5d38e34566810cd2"
```

### Case 3: hash_empty

**Description:** Hash empty bytes

```yaml
case_id: hash_empty
bindings:
  input_bytes: "0x"

expected:
  hash_hex: "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
```
