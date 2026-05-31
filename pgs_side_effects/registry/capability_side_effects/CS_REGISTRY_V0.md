# CS_REGISTRY_V0

## Header (Mandatory)

- **Artifact Code:** CS_REGISTRY_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Provide a registry capability for stable indirection by binding symbolic keys to opaque addresses and underlying storage references.

This capability allows:
- Registering new key-to-address bindings
- Resolving keys or addresses to storage targets
- Checking existence of registrations
- Deregistering keys via tombstone records

---

## 2. Rationale

Some workflows require:
- Stable addressing that survives storage reorganization
- Human-readable keys mapped to content-addressable hashes
- Symbolic links across storage capabilities
- Name service functionality

This CS exists as a meta-capability that coordinates access to other storage capabilities through stable indirection.

---

## 3. Applicability & Non-Applicability

### Valid Use Cases
- Address book: map kyc_key to user_id in user index
- Name service: map DNS-like names to storage locations
- Content addressing: map human keys to content hashes
- Symbolic links: stable references across storage reorganization

### Invalid Use Cases
- Direct data storage (use CS_MUTABLE_JSON_V0)
- Event logs (use CS_APPENDONLY_JSONL_V0)
- Mutable bindings (bindings are immutable)
- Re-binding existing keys

---

## 4. Side-Effect Category

- **Category:** Registry / Indirection
- **Side-Effect Type:** persistent
- **Append Semantics:** YES (append-only bindings)
- **Overwrite Semantics:** NO (immutable bindings)

---

## 5. Properties

| Property | Value | Description |
|----------|-------|-------------|
| durability | persistent | State survives restarts |
| idempotent | false | REGISTER is not idempotent |
| replay_policy | append_once | Replays may conflict |
| transactional | false | No atomic batch support |
| concurrent_safe | register_once | Key uniqueness enforced |

---

## 6. Guarantees

This CS guarantees:
- `stable_addressing` — addresses do not change
- `key_uniqueness` — each key maps to exactly one address
- `deterministic_address_generation` — same inputs produce same address
- `deterministic_resolution` — resolution is consistent
- `durable_across_restarts` — persisted to storage
- `append_only_bindings` — bindings are only added, never modified
- `immutable_bindings` — existing bindings cannot be changed
- `tombstone_based_deregistration` — deletions are append-only tombstones

---

## 7. Non-Guarantees

This CS does NOT guarantee:
- `data_storage` — only stores references, not data
- `data_validation` — does not validate referenced data
- `data_transformation` — does not transform data
- `ordering_guarantees` — no ordering of registrations
- `history_tracking` — no history of binding changes
- `audit_trail` — no audit log
- `rebinding_support` — cannot rebind existing keys
- `deterministic_replay_on_failure` — failures may not be replayable
- `garbage_collection` — tombstoned entries remain in log

---

## 8. Constraints

| Constraint | Value | Description |
|------------|-------|-------------|
| mutability | append_only | Bindings can only be added |
| key_scope | global | Keys are globally unique |
| max_key_length | 256 | Maximum key string length |
| address_format | content_addressable_hash | Addresses are deterministic hashes |
| deregistration_model | tombstone | Deletions append tombstone records |

---

## 9. Operations

### 9.1 REGISTER
Register a new key to (address, target_cs, target_ref) binding.

- **Input:** `key` (string, required), `target_cs` (string, required), `target_ref` (string, required)
- **Output:** `result_status`, `address`
- **Idempotent:** false
- **Result Status Values:** SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR
- **Note:** Creates immutable binding. Key must be unique. Returns deterministic address.

### 9.2 RESOLVE
Resolve a key or address to its storage target.

- **Input:** `key_or_address` (string, required)
- **Output:** `result_status`, `target_cs`, `target_ref`
- **Idempotent:** true
- **Result Status Values:** SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR
- **Note:** Accepts either symbolic key or opaque address. Returns where data is actually stored.

### 9.3 EXISTS
Check if a key or address is registered.

- **Input:** `key_or_address` (string, required)
- **Output:** `result_status`, `exists` (boolean)
- **Idempotent:** true
- **Result Status Values:** SUCCESS, VIOLATION, BACKEND_ERROR
- **Note:** Returns boolean exists flag

### 9.4 DEREGISTER
Mark a key or address as deregistered (append tombstone).

- **Input:** `key_or_address` (string, required)
- **Output:** `result_status`
- **Idempotent:** true
- **Result Status Values:** SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR
- **Note:** Append-only deletion (tombstone record). Idempotent — repeated calls return SUCCESS.

### 9.5 COUNT
Count active (non-tombstoned) registry entries.

- **Input:** (none)
- **Output:** `result_status`, `count` (integer)
- **Idempotent:** true
- **Result Status Values:** SUCCESS, BACKEND_ERROR
- **Note:** Returns the number of currently active bindings (tombstoned entries excluded).

---

## 10. Failure Semantics

### Failure Modes

| Status | Condition | Error Type |
|--------|-----------|------------|
| VIOLATION | Key fails validation (type, format, empty) | InvalidKey |
| ALREADY_EXISTS | Key already registered | DuplicateKey |
| NOT_FOUND | Key or address not registered | KeyNotFound |
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
| path | string | true | Filesystem path to JSONL registry file (append-only) |

**Note:** Configuration is provided via environment binding, not embedded in artifacts.

---

## 13. Architecture

### Role
Meta-capability for indirection

### Purpose
Provides stable symbolic addressing layer above concrete storage

### Binding Structure

| Field | Description | Example |
|-------|-------------|---------|
| key | Human-readable symbolic identifier | `Alice\|Doe\|alice@example.com` |
| address | Opaque content-addressable hash | `reg_a3f2c1...` |
| target_cs | Which storage capability holds the actual data | `CS_MUTABLE_JSON_V0` |
| target_ref | Reference within that capability | `user_001` |

---

## 14. Structural Checklist

- [x] No environment data embedded in artifacts
- [x] All operations declared with inputs/outputs
- [x] All result_status values declared
- [x] Failure modes explicit
- [x] Observability declared
- [x] Configuration schema declared

---

## Machine

```yaml
cs_code: CS_REGISTRY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Registry for stable indirection by binding symbolic keys to opaque addresses
  category: storage

  policy:
    operations: [REGISTER, RESOLVE, EXISTS, DEREGISTER, COUNT]

  operations:
    REGISTER:
      summary: Register a new key to address binding
      handler: register
      input: [key, target_cs, target_ref]
      output: [result_status, address]
      idempotent: false
      result_status_values: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]

    RESOLVE:
      summary: Resolve a key or address to its storage target
      handler: resolve
      input: [key_or_address]
      output: [result_status, target_cs, target_ref]
      idempotent: true
      result_status_values: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

    EXISTS:
      summary: Check if a key or address is registered
      handler: exists
      input: [key_or_address]
      output: [result_status, exists]
      idempotent: true
      result_status_values: [SUCCESS, VIOLATION, BACKEND_ERROR]

    DEREGISTER:
      summary: Mark a key or address as deregistered via tombstone
      handler: deregister
      input: [key_or_address]
      output: [result_status]
      idempotent: true
      result_status_values: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

    COUNT:
      summary: Count active (non-tombstoned) registry entries
      handler: count
      input: []
      output: [result_status, count]
      idempotent: true
      result_status_values: [SUCCESS, BACKEND_ERROR]

implementation:
  module: pgs_side_effects.implementation.side_effects.persistent.CS_REGISTRY_V0.runtime
  callable: RegistryRuntime

extensions:
  cs_kind: registry
  side_effect_type: persistent

  properties:
    durability: persistent
    idempotent: false
    replay_policy: append_once
    transactional: false
    concurrent_safe: register_once

  constraints:
    mutability: append_only
    key_scope: global
    max_key_length: 256
    address_format: content_addressable_hash
    deregistration_model: tombstone

  vocabulary:
    result_status: [SUCCESS, NOT_FOUND, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    key_validation_result: [VALID, INVALID]

  configuration_schema:
    path:
      type: string
      required: true
      description: Filesystem path to JSONL registry file (append-only)

  failure_modes:
    - "VIOLATION: Invalid key (type, format, empty)"
    - "ALREADY_EXISTS: Key already registered"
    - "NOT_FOUND: Key or address not registered"
    - "BACKEND_ERROR: Storage unavailable or corrupt"

  architecture:
    role: Meta-capability for indirection
    purpose: Provides stable symbolic addressing layer above concrete storage
    bindings:
      key: Human-readable symbolic identifier
      address: Opaque content-addressable hash
      target_cs: Which storage capability holds the actual data
      target_ref: Reference within that capability

  use_cases:
    - "Address book: map kyc_key to user_id in user index"
    - "Name service: map DNS-like names to storage locations"
    - "Content addressing: map human keys to content hashes"
    - "Symbolic links: stable references across storage reorganization"
```
