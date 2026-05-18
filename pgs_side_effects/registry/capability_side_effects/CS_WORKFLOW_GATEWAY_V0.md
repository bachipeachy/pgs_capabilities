# CS_WORKFLOW_GATEWAY_V0

## Header

- **Artifact Code:** CS_WORKFLOW_GATEWAY_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:** NONE

---

## 1. Intent

Provide a governed side-effect for invoking workflows via the execution gateway. This CS wraps `workflow_gateway.execute_workflow()` as a declarative operation.

**Ownership:** This is an infrastructure-owned CS. Transport only binds to it via runtime bindings.

## 2. Side-Effect Category

- **Category:** Execution Gateway
- **Side-Effect Type:** internal
- **Idempotent:** false (workflows may have side effects)

## 3. Operations

### 3.1 EXECUTE

Execute a workflow by code and return the execution result.

- **Input:** `workflow_code` (string, required), `payload` (object, required)
- **Output:** `result_status`, `execution_result`
- **Result Status Values:** SUCCESS, NOT_FOUND, BACKEND_ERROR

---

## Machine

```yaml
cs_code: CS_WORKFLOW_GATEWAY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Execute a workflow via the gateway
  category: execution_gateway

  policy:
    operations: [EXECUTE]

  operations:
    EXECUTE:
      summary: Execute a workflow by code
      handler: execute
      input: [workflow_code, payload]
      output: [result_status, execution_result]
      idempotent: false
      result_status_values: [SUCCESS, NOT_FOUND, BACKEND_ERROR]

implementation:
  module: pgs_side_effects.implementation.side_effects.internal.CS_WORKFLOW_GATEWAY_V0.runtime
  callable: WorkflowGatewayRuntime

extensions:
  cs_kind: execution_gateway
  side_effect_type: internal

  vocabulary:
    result_status: [SUCCESS, NOT_FOUND, BACKEND_ERROR]

  configuration_schema:
    default_runtime_binding:
      type: string
      required: true
      description: RB code for the inner workflow execution
```
