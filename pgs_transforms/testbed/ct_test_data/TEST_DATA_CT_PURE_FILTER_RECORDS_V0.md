# TEST_DATA_CT_PURE_FILTER_RECORDS_V0

## Machine

```yaml
test_data_code: capability_transforms::TEST_DATA_CT_PURE_FILTER_RECORDS_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_FILTER_RECORDS_V0
  description: |
    Test array filtering by field criteria (exact-value match and field-presence checks).
  target_artifact: CT_PURE_FILTER_RECORDS_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_FILTER_RECORDS_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_FILTER_RECORDS_V0
ct_fqdn: "transforms.capability_transforms::CT_PURE_FILTER_RECORDS_V0"
```

## Purpose

Test array filtering by exact-value match, field-presence check, and multi-criterion AND logic.

## Test Cases

### Case 1: filter_by_exact_value

**Description:** Filter array to records matching a single exact field value

```yaml
case_id: filter_by_exact_value
expected_outcome: SUCCESS
bindings:
  source:
    - {actor_id: "AC_aaa", enrollment_status: "ACTIVE", stake: "32000000000"}
    - {actor_id: "AC_bbb", enrollment_status: "INACTIVE", stake: "32000000000"}
    - {actor_id: "AC_ccc", enrollment_status: "ACTIVE", stake: "16000000000"}
  filter:
    enrollment_status: "ACTIVE"

expected:
  extracted:
    - {actor_id: "AC_aaa", enrollment_status: "ACTIVE", stake: "32000000000"}
    - {actor_id: "AC_ccc", enrollment_status: "ACTIVE", stake: "16000000000"}
```

### Case 2: filter_by_field_presence

**Description:** Filter to records where a field exists and is non-null

```yaml
case_id: filter_by_field_presence
expected_outcome: SUCCESS
bindings:
  source:
    - {tx_id: "TX_001", status: "PENDING"}
    - {tx_id: "TX_002"}
    - {tx_id: "TX_003", status: "PENDING"}
  filter:
    status: "present"

expected:
  extracted:
    - {tx_id: "TX_001", status: "PENDING"}
    - {tx_id: "TX_003", status: "PENDING"}
```

### Case 3: filter_multi_criteria

**Description:** Filter by multiple criteria — AND logic; all must be satisfied

```yaml
case_id: filter_multi_criteria
expected_outcome: SUCCESS
bindings:
  source:
    - {actor_id: "AC_aaa", enrollment_status: "ACTIVE", stake: "32000000000"}
    - {actor_id: "AC_bbb", enrollment_status: "ACTIVE", stake: "16000000000"}
    - {actor_id: "AC_ccc", enrollment_status: "INACTIVE", stake: "32000000000"}
  filter:
    enrollment_status: "ACTIVE"
    stake: "32000000000"

expected:
  extracted:
    - {actor_id: "AC_aaa", enrollment_status: "ACTIVE", stake: "32000000000"}
```

### Case 4: filter_single_match

**Description:** Filter returns exactly one matching record from mixed source

```yaml
case_id: filter_single_match
expected_outcome: SUCCESS
bindings:
  source:
    - {id: "R1", type: "validator", active: true}
    - {id: "R2", type: "observer", active: true}
    - {id: "R3", type: "validator", active: false}
  filter:
    type: "validator"
    active: true

expected:
  extracted:
    - {id: "R1", type: "validator", active: true}
```
