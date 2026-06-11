# CS_CONCURRENT_WORKFLOWS_V0

## Header

- **Artifact Code:** CS_CONCURRENT_WORKFLOWS_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:** NONE

---

## 1. Intent

Execute a declared set of workflows concurrently and collect all results. Completion ordering is not guaranteed. All workflows run to completion regardless of individual outcomes — no short-circuit on VIOLATION.

**Ownership:** Infrastructure-owned CS. Domain CCs bind to it via runtime bindings.

---

## 2. Side-Effect Category

- **Category:** Execution Gateway
- **Side-Effect Type:** internal
- **Idempotent:** false (WF invocations have side effects)

---

## 3. Operations

### 3.1 EXECUTE_CONCURRENT

Invoke all declared workflows. All execute; none are skipped due to peer outcomes.

**Input fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflows` | array | YES | Ordered list of WF invocation specs; each entry: `{code: FQDN, payload: object}`; each `code` must be unique within a single invocation |
| `triggered_by` | string | YES | Actor ID — available for injection into WF payloads |

**Output fields:**

| Field | Type | Description |
|-------|------|-------------|
| `results` | array | One entry per invoked WF: `{code: FQDN, result_status: string, outputs: object}`; correlated by `code` field, NOT by array position |
| `all_succeeded` | boolean | `true` iff every WF returned `SUCCESS`; `false` if any returned `VIOLATION` or `BACKEND_ERROR` |

**Result Status Values:** `SUCCESS`, `PARTIAL_FAILURE`, `BACKEND_ERROR`

**Contract invariants:**
- Workflow completion ordering is not guaranteed.
- Results are correlated by `code` (workflow FQDN) — callers must use `code` as the lookup key, not array index.
- All declared workflows execute; VIOLATION in one does not halt peers.
- Duplicate `code` values within a single invocation are a VIOLATION.

---

## Machine

```yaml
cs_code: CS_CONCURRENT_WORKFLOWS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Execute a declared set of workflows concurrently and collect all results
  category: execution_gateway

  policy:
    operations: [EXECUTE_CONCURRENT]

  operations:
    EXECUTE_CONCURRENT:
      summary: Invoke all declared workflows concurrently; collect results correlated by code
      handler: execute
      input: [workflows, triggered_by]
      output: [results, all_succeeded]
      idempotent: false
      result_status_values: [SUCCESS, PARTIAL_FAILURE, BACKEND_ERROR]

implementation:
  module: pgs_side_effects.implementation.side_effects.internal.CS_CONCURRENT_WORKFLOWS_V0.runtime
  callable: ConcurrentWorkflowsRuntime

extensions:
  cs_kind: execution_gateway
  side_effect_type: internal

  vocabulary:
    result_status: [SUCCESS, PARTIAL_FAILURE, BACKEND_ERROR]

  notes:
    - workflow_executor injected at runtime by the dispatcher — not declarable in JSON policy
    - Zero domain knowledge — all WF codes and payloads declared by the calling CC
    - All workflows execute regardless of peer outcomes — no short-circuit
    - Results correlated by code (workflow FQDN), NOT by array position
    - Duplicate code values in a single invocation → VIOLATION
    - BACKEND_ERROR if workflow_executor raises an unhandled exception
```
