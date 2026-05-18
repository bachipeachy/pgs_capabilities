# TEST_DATA_CT_PURE_GENERATE_ID_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_GENERATE_ID_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_GENERATE_ID_V0
  description: |
    Test deterministic ID generation using Keccak-256 hashing.
  target_artifact: CT_PURE_GENERATE_ID_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_GENERATE_ID_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_GENERATE_ID_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_GENERATE_ID_V0"
```

## Purpose

Test deterministic ID generation using Keccak-256 hashing.

## Test Cases

### Case 1: generate_id_string_data

**Description:** Generate ID from string data

```yaml
case_id: generate_id_string_data
bindings:
  prefix: "AC"
  data: "test_account"

expected:
  id: "AC_ac8cc683f338b84f"
```

### Case 2: generate_id_object_data

**Description:** Generate ID from object data

```yaml
case_id: generate_id_object_data
bindings:
  prefix: "WF"
  data:
    workflow: "build"
    version: "v1"

expected:
  id: "WF_75382b9a6ab93c66"
```

### Case 3: generate_id_numeric_data

**Description:** Generate ID from numeric data

```yaml
case_id: generate_id_numeric_data
bindings:
  prefix: "TX"
  data: 12345

expected:
  id: "TX_d3ff95909dfb2231"

```

### Case 4: generate_id_deterministic

**Description:** Verify same inputs produce same ID

```yaml
case_id: generate_id_deterministic
bindings:
  prefix: "IN"
  data: "consistent"

expected:
  id: "IN_c918e775137f8254"
```
