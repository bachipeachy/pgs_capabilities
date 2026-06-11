# pgs_capabilities

**Implementation surface for Protocol-Governed Systems.**

This repository contains the concrete implementations of capability transforms (CT) and side-effects (CS) declared in the protocol.  
It is where computation and IO happen.  
It is not where behavior is defined.

Behavior is declared in protocol, executed by runtime, implemented in capabilities, and observed via traces and state.

> **New to PGS?** This is one of the repositories in the Protocol-Governed Systems ecosystem.
> For orientation, architecture overview, and end-to-end execution, start at [pgs_workspace](https://github.com/bachipeachy/pgs_workspace).

---

## Role in the system

The PGS architecture separates three concerns cleanly:

```
pgs_governance  → defines invariants and constitutional rules
pgs_compiler    → compiles protocol artifacts into snapshot
pgs_runtime     → orchestrates how it is executed
pgs_capabilities → implements how it is performed within declared contracts
```

This repository covers the third layer. Implementations live here, but they operate within contracts defined entirely by the protocol. A CT or CS function cannot choose what happens next — it only executes its assigned unit of work.

---

## Capability types

### Capability Transform (CT)

Pure computation:
- deterministic
- no side-effects
- input → output, nothing else

**Examples from this repo:**
- `CT_PURE_DERIVE_WALLET_KEYPAIRS_V0` — derive a keypair from a seed
- `CT_PURE_BUILD_TRANSACTION_PAYLOAD_V0` — construct a transaction record
- `CT_PURE_NORMALIZE_ACTOR_INPUT_V0` — normalize and validate actor fields

### Capability Side Effect (CS)

Controlled interaction with state or external systems.  
Semantics are declared in the protocol, not inferred in code.

**Examples from this repo:**

| CS artifact | Behavior |
|-------------|----------|
| `CS_APPENDONLY_JSONL_V0` | Always appends — never overwrites |
| `CS_MUTABLE_JSON_V0` | Overwrites declared state |
| `CS_REGISTRY_INSERT_V0` | Enforces uniqueness → `ALREADY_EXISTS` on repeat |

---

## Binding model

CT/CS implementations are resolved at compile time, not at runtime.

```
CT/CS artifact (protocol) → implementation (this repo)
                          ↑
                   bound by RB_ (Runtime Binding) artifacts
```

At runtime there is:
- no dynamic lookup
- no plugin discovery
- no runtime registration

The runtime receives fully resolved bindings from the snapshot.

---

## Inputs → Outputs

**Inputs:**
- structured JSON from the workflow (via resolved JSONPath)
- bindings already resolved in `protocol_snapshot/`

**Outputs:**
- structured results matching the declared output schema
- side-effects applied to `data_root` (for CS implementations)

Outputs must match the declared contract exactly. The runtime enforces this.

---

## What implementations must obey

Each implementation is bound by its protocol declaration:
- declared inputs — accepted as-is, no re-interpretation
- declared outputs — returned as declared, no extras
- declared semantics — CS behaviors are structural, not optional

Implementations do not:
- access undeclared state
- choose the next step
- branch execution
- suppress outcomes
- interpret what their result means

**They return a result. The protocol defines its meaning. The runtime handles the rest.**

---

## Enforced purity boundaries

| Type | Rule |
|------|------|
| CT | Must be side-effect free |
| CS | Must obey declared storage semantics |

This separation is structural. A CT that writes state, or a CS that reroutes execution, is a design violation — not a feature.

---

## Example (conceptual)

Protocol declares a node that uses `CS_REGISTRY_INSERT_V0`.  
This repo provides:

```python
def cs_registry_insert(inputs, data_root):
    if record_exists(inputs["key"], data_root):
        return {"result_status": "ALREADY_EXISTS"}
    write_record(inputs, data_root)
    return {"result_status": "SUCCESS"}
```

Routing is not here. The outcome is returned. The compiled DAG decides what happens next.

---

## Repo structure

```
pgs_capabilities/
├── pgs_capabilities/    ← capability registry and compiled bindings
├── pgs_transforms/      ← CT implementations
│   ├── implementation/
│   ├── registry/
│   └── testbed/
└── pgs_side_effects/    ← CS implementations
    ├── implementation/
    ├── registry/
    └── testbed/
```

---

## What you should do here

- Implement new CTs (pure, deterministic logic)
- Implement new CSs (declared storage/IO semantics)
- Optimize existing implementations
- Add platform-specific or environment-specific bindings

## What you should NOT do here

- Define workflows
- Encode routing logic
- Introduce implicit behavior
- Bypass declared contracts

If behavior needs to change, change the protocol. If an implementation needs to "know" about the workflow it belongs to, that is a design violation.

---

## Where this fits in the system

| Repo | Role |
|------|------|
| `pgs_governance` + `pgs_compiler` | Declare and compile what must happen |
| `pgs_runtime` | Executes the compiled graph |
| **`pgs_capabilities` ← here** | **Implements CT/CS** |
| `pgs_blockchain` | Domain workflows that use these capabilities |
| `pgs_ai_governance` | Governance workflows that use these capabilities |
| `pgs_change_mgmt` | Governed SDLC — Change Request to Authoring Mandate (new in v0.5.0) |
| `pgs_workspace` | Entry point for execution |

---

## Research context

> *"Extensibility by declaration, not refactor."*

This repository demonstrates the third leg of that claim: because behavior is externalized into protocol, implementations are modular and replaceable. You can swap, optimize, or add platform-specific bindings without touching workflows or runtime.

---

## Final note

This is where work is done, not where decisions are made.

If a CT/CS implementation needs to know about the workflow it belongs to — stop.  
That knowledge belongs in the protocol.
---

## License

Apache-2.0. See LICENSE and NOTICE for details.
