# CS_NAME_REGISTRY_V0

## Header (Mandatory)

- **Artifact Code:** CS_NAME_REGISTRY_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Provide persistent storage for name-to-resource-address mappings, enabling human-readable names (e.g., email addresses) to resolve to public resource addresses.

This capability allows:
- Registering name → resource_addresses[] mappings
- Looking up resource addresses by name
- Domain-neutral address book functionality

---

## 2. Rationale

Workflows require stable, human-readable references to resources instead of hardcoded addresses. This CS provides:
- Name resolution (like DNS for resources)
- Public address book functionality
- Test determinism without hardcoded inputs

---

## 3. Applicability & Non-Applicability

### Valid Use Cases
- Map email addresses to blockchain addresses
- Resolve contact names to resource identifiers
- Enable human-readable transaction targets
- Test setup with stable name references

### Invalid Use Cases
- Direct data storage (use CS_MUTABLE_JSON_V0)
- Internal user/wallet ID mappings (must use public projections only)
- Complex filtering or ranking (belongs in domain logic)
- Authentication or identity management

---

## 4. Side-Effect Category

- **Category:** Storage / Mapping
- **Side-Effect Type:** persistent
- **Append Semantics:** NO
- **Overwrite Semantics:** YES (names can be updated)

---

## 5. Properties

| Property | Value | Description |
|----------|-------|-------------|
| durability | persistent | State survives restarts |
| idempotent | true | WRITE with same data is idempotent |
| replay_policy | last_write_wins | Overwrites allowed |
| transactional | false | No atomic batch support |
| concurrent_safe | false | No coordination for concurrent writes |

---

## 6. Guarantees

This CS guarantees:
- `persistent_storage` — data survives restarts
- `deterministic_lookup` — same name returns same addresses
- `durable_across_restarts` — persisted to storage
- `public_projection_only` — no internal IDs exposed

---

## 7. Non-Guarantees

This CS does NOT guarantee:
- `data_validation` — does not validate address formats
- `name_validation` — does not enforce name format rules
- `ordering_guarantees` — no ordering of addresses in array
- `history_tracking` — no history of changes
- `audit_trail` — no audit log
- `concurrent_write_safety` — last write wins
- `atomic_batch_operations` — no batch support
- `referential_integrity` — does not verify addresses exist

---

## 8. Constraints

| Constraint | Value | Description |
|------------|-------|-------------|
| mutability | read_write | Names can be created and updated |
| name_format | string | Any valid string (typically email) |
| max_name_length | 256 | Maximum name string length |
| address_format | string_array | Array of public address strings |
| max_addresses_per_name | 100 | Maximum addresses per name |

---

## 9. Operations

### 9.1 READ

Look up resource addresses for a given name.

- **Input:** `name` (string, required)
- **Output:** `result_status`, `resource_addresses` (array of strings)
- **Idempotent:** true
- **Result Status Values:** SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR
- **Note:** Returns empty array if name not found (NOT_FOUND status)

### 9.2 WRITE

Register or update name → resource_addresses mapping.

- **Input:** `name` (string, required), `resource_addresses` (array of strings, required)
- **Output:** `result_status`, `success` (boolean)
- **Idempotent:** true (same data)
- **Result Status Values:** SUCCESS, VIOLATION, BACKEND_ERROR
- **Note:** Overwrites existing mapping if name exists. Creates new if not exists.

---

## 10. Failure Semantics

### Failure Modes

| Status | Condition | Error Type |
|--------|-----------|------------|
| VIOLATION | Name empty or invalid type | InvalidName |
| VIOLATION | Addresses not array or invalid type | InvalidAddresses |
| NOT_FOUND | Name not registered (READ only) | NameNotFound |
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

**Note:** Configuration is provided via runtime binding, not embedded in artifacts.

---

## 13. Data Model

**Storage Format:** JSON object with name keys mapping to address arrays

```json
{
  "alice@example.com": {
    "resource_addresses": [
      "0xABC123...",
      "0xDEF456..."
    ]
  },
  "bob@example.com": {
    "resource_addresses": [
      "0x789GHI..."
    ]
  }
}
```

**Constraints:**
- Name = primary key (string)
- Values = object with `resource_addresses` array field
- No internal identifiers (user_id, wallet_id, etc.) allowed
- All addresses are public, external references

---

## 14. Architecture

### Role
Public name resolution capability

### Purpose
Maps human-readable names to public resource addresses

### Public Projection
Only exposes:
- Names (human-readable identifiers)
- Resource addresses (public addresses)

Does NOT expose:
- Internal user IDs
- Internal wallet IDs
- Private keys
- Internal references

---

## 15. Structural Checklist

- [x] No environment data embedded in artifacts
- [x] All operations declared with inputs/outputs
- [x] All result_status values declared
- [x] Failure modes explicit
- [x] Observability declared
- [x] Configuration schema declared
- [x] Public projection only (no internal IDs)

---

## Machine

```yaml
cs_code: CS_NAME_REGISTRY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Persistent storage for name-to-resource-address mappings
  category: storage

  policy:
    operations: [READ, WRITE]

  operations:
    READ:
      summary: Look up resource addresses for a given name
      handler: read
      input: [name]
      output: [result_status, resource_addresses]
      idempotent: true
      result_status_values: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

    WRITE:
      summary: Register or update name to resource addresses mapping
      handler: write
      input: [name, resource_addresses]
      output: [result_status, success]
      idempotent: true
      result_status_values: [SUCCESS, VIOLATION, BACKEND_ERROR]

implementation:
  module: pgs_side_effects.implementation.side_effects.persistent.CS_NAME_REGISTRY_V0.runtime
  callable: NameRegistryRuntime

extensions:
  cs_kind: storage
  side_effect_type: persistent

  properties:
    durability: persistent
    idempotent: true
    replay_policy: last_write_wins
    transactional: false
    concurrent_safe: false

  constraints:
    mutability: read_write
    name_format: string
    max_name_length: 256
    address_format: string_array
    max_addresses_per_name: 100

  vocabulary:
    result_status: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

  configuration_schema:
    path:
      type: string
      required: true
      description: Filesystem path to JSON storage file

  failure_modes:
    - "VIOLATION: Name empty or invalid type"
    - "VIOLATION: Addresses not array or invalid type"
    - "NOT_FOUND: Name not registered (READ only)"
    - "BACKEND_ERROR: Storage unavailable or corrupt"

  architecture:
    role: Public name resolution capability
    purpose: Maps human-readable names to public resource addresses
    public_projection:
      exposes: [names, resource_addresses]
      does_not_expose: [user_id, wallet_id, internal_keys]
```
