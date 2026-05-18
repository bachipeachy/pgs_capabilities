# CS_MUTABLE_JSON_V0

## Header (Mandatory)

- **Artifact Code:** CS_MUTABLE_JSON_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Provide a mutable key-addressable JSON state store with last-write-wins semantics.

This capability allows:
- Reading values by key
- Writing/overwriting values at keys
- Deleting keys
- Checking key existence
- Listing all keys

---

## 2. Rationale

Some workflows require state that:
- Evolves over time
- Reflects latest values only (not history)
- Is not append-only
- Supports idempotent operations

This CS exists to explicitly permit controlled mutation with clear semantics.

---

## 3. Applicability & Non-Applicability

### Valid Use Cases
- State snapshots
- Current status records
- Idempotent updates
- Configuration storage
- Session state

### Invalid Use Cases
- Audit logs (use CS_APPENDONLY_JSONL_V0)
- Event sourcing (use CS_APPENDONLY_JSONL_V0)
- Historical reconstruction
- Concurrent multi-writer scenarios
- Transactional batch operations

---

## 4. Side-Effect Category

- **Category:** Mutable State
- **Side-Effect Type:** persistent
- **Append Semantics:** NO
- **Overwrite Semantics:** YES (last-write-wins)

---

## 5. Properties

| Property | Value | Description |
|----------|-------|-------------|
| durability | persistent | State survives restarts |
| idempotent | true | All operations are idempotent |
| replay_policy | safe_replay | Idempotent ops can be retried |
| transactional | false | No atomic batch support |
| concurrent_safe | false | Single-writer model |

---

## 6. Guarantees

This CS guarantees:
- `mutable` — values can be changed
- `last_write_wins` — no conflict resolution, latest write prevails
- `json_format` — values stored as JSON
- `durable_across_restarts` — persisted to storage
- `key_addressable` — values accessed by string key
- `idempotent_operations` — safe to retry

---

## 7. Non-Guarantees

This CS does NOT guarantee:
- `ordering` — no ordering of writes
- `history` — no historical versions
- `audit` — no audit trail
- `versioning` — no version tracking
- `conflict_resolution` — no merge strategies
- `multi_version_concurrency_control` — no MVCC
- `atomic_batch_operations` — no transactions

---

## 8. Constraints

| Constraint | Value | Description |
|------------|-------|-------------|
| concurrency | single_writer | One writer at a time |
| max_key_length | 256 | Maximum key string length |
| max_value_size_mb | 10 | Maximum value size in MB |

---

## 9. Operations

### 9.1 GET
Retrieve value for a given key.

- **Input:** `key` (string, required)
- **Output:** `result_status`, `value`
- **Idempotent:** true
- **Result Status Values:** SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR

### 9.2 PUT
Store or update a value at the given key.

- **Input:** `key` (string, required), `value` (object, required)
- **Output:** `result_status`
- **Idempotent:** true
- **Result Status Values:** SUCCESS, VIOLATION, BACKEND_ERROR
- **Note:** Last-write-wins — overwrites existing value

### 9.3 DELETE
Remove the given key and its value.

- **Input:** `key` (string, required)
- **Output:** `result_status`
- **Idempotent:** true
- **Result Status Values:** SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR

### 9.4 EXISTS
Check if a key exists in storage.

- **Input:** `key` (string, required)
- **Output:** `result_status`, `exists` (boolean)
- **Idempotent:** true
- **Result Status Values:** SUCCESS, VIOLATION, BACKEND_ERROR

### 9.5 LIST
List all keys in storage.

- **Input:** (none)
- **Output:** `result_status`, `keys` (array of strings)
- **Idempotent:** true
- **Result Status Values:** SUCCESS, BACKEND_ERROR

---

## 10. Failure Semantics

### Failure Modes

| Status | Condition | Error Type |
|--------|-----------|------------|
| VIOLATION | Key fails validation (type, format, empty) | InvalidKey |
| NOT_FOUND | Requested key does not exist | KeyNotFound |
| BACKEND_ERROR | Storage unavailable or corrupt | StorageUnavailable, StorageCorrupt |

### Behavior
- All failures are **fail-loud** — no silent failures
- All failures emit trace events
- All failures return explicit `result_status`

---

## 11. Observability Guarantees

This CS MUST emit:
- `cs_start` — operation invocation begins
- `cs_success` — operation completed with SUCCESS
- `cs_failure` — operation completed with non-SUCCESS status

---

## 12. Configuration Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| path | string | true | Filesystem path to JSON storage file |

**Note:** Configuration is provided via environment binding, not embedded in artifacts.

---

## 13. Structural Checklist

- [x] No environment data embedded in artifacts
- [x] All operations declared with inputs/outputs
- [x] All result_status values declared
- [x] Failure modes explicit
- [x] Observability declared
- [x] Configuration schema declared

---

## Machine

```yaml
cs_code: CS_MUTABLE_JSON_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Mutable key-addressable JSON state store with last-write-wins semantics
  category: storage

  policy:
    operations: [GET, PUT, DELETE, EXISTS, LIST]

  operations:
    GET:
      summary: Retrieve value for a given key
      handler: read
      input: [key]
      output: [result_status, value]
      idempotent: true
      result_status_values: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

    PUT:
      summary: Store or update a value at the given key
      handler: write
      input: [key, value]
      output: [result_status]
      idempotent: true
      result_status_values: [SUCCESS, VIOLATION, BACKEND_ERROR]

    DELETE:
      summary: Remove the given key and its value
      handler: delete
      input: [key]
      output: [result_status]
      idempotent: true
      result_status_values: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

    EXISTS:
      summary: Check if a key exists in storage
      handler: exists
      input: [key]
      output: [result_status, exists]
      idempotent: true
      result_status_values: [SUCCESS, VIOLATION, BACKEND_ERROR]

    LIST:
      summary: List all keys in storage
      handler: list_keys
      input: []
      output: [result_status, keys]
      idempotent: true
      result_status_values: [SUCCESS, BACKEND_ERROR]

implementation:
  module: pgs_side_effects.implementation.side_effects.persistent.CS_MUTABLE_JSON_V0.runtime
  callable: MutableJsonRuntime

extensions:
  cs_kind: mutable_state
  side_effect_type: persistent

  properties:
    durability: persistent
    idempotent: true
    replay_policy: safe_replay
    transactional: false
    concurrent_safe: false

  constraints:
    concurrency: single_writer
    max_key_length: 256
    max_value_size_mb: 10

  vocabulary:
    result_status: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

  configuration_schema:
    path:
      type: string
      required: true
      description: Filesystem path to JSON storage file

  failure_modes:
    - "VIOLATION: Invalid key (type, format, empty)"
    - "NOT_FOUND: Key does not exist"
    - "BACKEND_ERROR: Storage unavailable or corrupt"
```
