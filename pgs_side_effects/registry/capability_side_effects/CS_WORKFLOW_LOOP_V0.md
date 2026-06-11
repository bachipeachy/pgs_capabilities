# CS_WORKFLOW_LOOP_V0

## Header

- **Artifact Code:** CS_WORKFLOW_LOOP_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:** NONE

---

## 1. Intent

Execute a finite sequence of governed WF invocations using a declarative dispatch spec (Collatz loop pattern). Zero domain knowledge — the declaring CC provides all dispatch logic as inputs. This CS is the substrate mechanism that enables the Collatz pattern for loop-absorbing CCs.

**Ownership:** Infrastructure-owned CS. Domain CCs bind to it via runtime bindings.

---

## 2. Side-Effect Category

- **Category:** Execution Gateway
- **Side-Effect Type:** internal
- **Idempotent:** false (WF invocations have side effects)

---

## 3. Operations

### 3.1 EXECUTE_SEQUENCE

Iterate over a `sequence` array. For each item:
1. For each sub-item in the item's declared sub-sequence field, resolve the WF code from a key-field dispatch mapping and invoke it.
2. Invoke the declared `item_wf` with fields mapped from the item.

All dispatch logic (WF codes, field mappings, key-field routing) is declared by the calling CC in the input payload — this CS has zero domain knowledge.

**Input fields:**

| Field | Type | Description |
|-------|------|-------------|
| sequence | array | Ordered list of items to iterate |
| triggered_by | string | Actor ID — available for injection into item WF payloads |
| item_wf | object | `{code, payload_fields, inject}` — WF to invoke per item |
| item_sub_sequence | object | `{field, wf_dispatch: {key_field, mapping}, payload_fields}` — sub-sequence dispatch spec |

**item_wf fields:**
- `code` — FQDN of the WF to invoke for each item; mutually exclusive with `wf_dispatch`
- `wf_dispatch` — `{key_field, mapping}` — resolves WF code from `item[key_field]`; mutually exclusive with `code`
- `payload_fields` — `{dest_field: source_field_in_item}` mapping; omit when using `wf_dispatch` to pass entire item as payload
- `inject` — `{field: literal_value}` — constants injected into item WF payload

**Governance rule:** Exactly one of `code` or `wf_dispatch` must be supplied in `item_wf`.

**item_sub_sequence fields:**
- `field` — name of the array field within each item
- `wf_dispatch.key_field` — field in each sub-item used to select WF code
- `wf_dispatch.mapping` — `{key_value: wf_fqdn}` dispatch table
- `payload_fields` — `{dest_field: source_field_in_sub_item}` mapping; omit to pass entire sub-item

**Output fields:**

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | SUCCESS / VIOLATION / BACKEND_ERROR |
| items_processed | integer | Number of items from sequence that completed successfully |
| sub_items_processed | integer | Total sub-items processed across all items |

**Result Status Values:** SUCCESS, VIOLATION, BACKEND_ERROR

**Failure semantics:**
- VIOLATION from any WF invocation halts the loop and propagates immediately
- Unknown key in wf_dispatch.mapping → VIOLATION
- BACKEND_ERROR on executor failure

---

## Machine

```yaml
cs_code: CS_WORKFLOW_LOOP_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Execute a finite sequence of governed WF invocations via declarative dispatch spec
  category: execution_gateway

  policy:
    operations: [EXECUTE_SEQUENCE]

  operations:
    EXECUTE_SEQUENCE:
      summary: Iterate sequence; invoke item_wf per item and dispatch sub-items by key-field mapping
      handler: execute
      input: [sequence, triggered_by, item_wf, item_sub_sequence]
      output: [result_status, items_processed, sub_items_processed]
      idempotent: false
      result_status_values: [SUCCESS, VIOLATION, BACKEND_ERROR]

implementation:
  module: pgs_side_effects.implementation.side_effects.internal.CS_WORKFLOW_LOOP_V0.runtime
  callable: WorkflowLoopRuntime

extensions:
  cs_kind: execution_gateway
  side_effect_type: internal

  vocabulary:
    result_status: [SUCCESS, VIOLATION, BACKEND_ERROR]

  notes:
    - workflow_executor injected at runtime by the dispatcher — not declarable in JSON policy
    - Zero domain knowledge — all WF codes and field mappings declared by the calling CC
    - Sub-sequence processed BEFORE item_wf (transactions before block proposal per slot)
    - VIOLATION halts the loop immediately — no partial commit
    - payload_fields omitted in item_sub_sequence → entire sub-item passed as payload
    - item_wf.code and item_wf.wf_dispatch are mutually exclusive; exactly one must be supplied
    - item_wf.wf_dispatch — resolves WF code from item[key_field]; payload_fields omitted → entire item passed as payload
```
