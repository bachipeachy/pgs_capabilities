# CS_APPENDONLY_JSONL_V0

## Header (Mandatory)

- **Artifact Code:** CS_APPENDONLY_JSONL_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Provide an append-only JSONL persistence layer with ordered event history.

This capability allows:
- Appending records to the end of a log
- Reading all records in order

---

## 2. Rationale

Some workflows require state that:
- Is immutable once written
- Preserves complete history
- Maintains strict ordering
- Supports event sourcing patterns
- Enables audit trails

This CS exists to explicitly permit append-only writes with clear ordering semantics.

---

## 3. Applicability & Non-Applicability

### Valid Use Cases
- Audit logs
- Event sourcing
- Transaction history
- Activity streams
- Ledger entries
- Historical reconstruction

### Invalid Use Cases
- Mutable state (use CS_MUTABLE_JSON_V0)
- Key-value lookups (use CS_MUTABLE_JSON_V0)
- State snapshots requiring updates
- Data that needs deletion
- Random access patterns

---

## 4. Side-Effect Category

- **Category:** Append-Only Log
- **Side-Effect Type:** persistent
- **Append Semantics:** YES (ordered, monotonic)
- **Overwrite Semantics:** NO

---

## 5. Properties

| Property | Value | Description |
|----------|-------|-------------|
| durability | persistent | State survives restarts |
| idempotent | false | APPEND creates new entry each time |
| replay_policy | append_once | Replays create duplicate entries |
| transactional | false | No atomic batch support |
| concurrent_safe | false | Single-writer model |

---

## 6. Guarantees

This CS guarantees:
- `append_only` — records cannot be modified or deleted
- `ordered` — records maintain strict append order
- `jsonl_format` — records stored as JSON Lines
- `durable_across_restarts` — persisted to storage

---

## 7. Non-Guarantees

This CS does NOT guarantee:
- `mutation` — no updates to existing records
- `overwrite` — no replacement of records
- `random_access` — no direct key-based lookup
- `deletion` — no removal of records
- `key_addressability` — no key-value semantics
- `exactly_once_delivery` — retries create duplicates

---

## 8. Constraints

| Constraint | Value | Description |
|------------|-------|-------------|
| concurrency | single_writer | One writer at a time |
| max_record_size_mb | 10 | Maximum record size in MB |

---

## 9. Operations

### 9.1 APPEND
Append a record to the end of the log.

- **Input:** `record` (object, required), `stream_id` (string, required), `actor_id` (string, required)
- **Output:** `result_status`, `record_id`, `sequence_number`
- **Idempotent:** false
- **Result Status Values:** SUCCESS, VIOLATION, BACKEND_ERROR
- **Note:** NOT idempotent — each call creates a new entry

### 9.2 GET_ALL
Retrieve all records from the log.

- **Input:** `stream_id` (string, required)
- **Output:** `result_status`, `entries`
- **Idempotent:** true
- **Result Status Values:** SUCCESS, BACKEND_ERROR
- **Note:** Returns array of all entries in append order

---

## 10. Failure Semantics

### Failure Modes

| Status | Condition | Error Type |
|--------|-----------|------------|
| VIOLATION | Record fails validation (type, format) | InvalidRecord |
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
| path | string | true | Filesystem path to JSONL storage file |

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
cs_code: CS_APPENDONLY_JSONL_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Append-only JSONL persistence layer with ordered event history
  category: storage

  policy:
    operations: [APPEND, GET_ALL]

  operations:
    APPEND:
      summary: Append a record to the end of the log
      handler: append
      input: [record, stream_id, actor_id]
      output: [result_status, record_id, sequence_number]
      idempotent: false
      result_status_values: [SUCCESS, VIOLATION, BACKEND_ERROR]

    GET_ALL:
      summary: Retrieve all records from the log
      handler: read_all
      input: [stream_id]
      output: [result_status, entries]
      idempotent: true
      result_status_values: [SUCCESS, BACKEND_ERROR]

implementation:
  module: pgs_side_effects.implementation.side_effects.persistent.CS_APPENDONLY_JSONL_V0.runtime
  callable: AppendOnlyJsonlRuntime

extensions:
  cs_kind: append_only_log
  side_effect_type: persistent

  properties:
    durability: persistent
    idempotent: false
    replay_policy: append_once
    transactional: false
    concurrent_safe: false

  constraints:
    concurrency: single_writer
    max_record_size_mb: 10

  vocabulary:
    result_status: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    entry_validation_result: [VALID, INVALID]

  configuration_schema:
    path:
      type: string
      required: true
      description: Filesystem path to JSONL storage file

  failure_modes:
    - "VIOLATION: Invalid record (type, format)"
    - "BACKEND_ERROR: Storage unavailable or corrupt"
```
