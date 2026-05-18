# WF_REGISTER_NAME_V0

## Header

- **Artifact Code:** WF_REGISTER_NAME_V0
- **Artifact Kind:** workflow
- **Governed By:** fb.topology::CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:** pgs_capabilities.registry.name_service.capability_contracts::CC_REGISTER_NAME_V0

---

## 1. Intent

Register or update name-to-resource-addresses mapping via protocol path.

---

## 2. Flow

```
entry → register → exit
```

Single-step workflow that invokes name registration capability contract.

---

## 3. Steps

### Step: register

- **Uses:** pgs_capabilities.registry.name_service.capability_contracts::CC_REGISTER_NAME_V0
- **Operation:** WRITE
- **Role:** Register or update name mapping

---

## 4. Entry and Exit

- **Entry Point:** register
- **Exit Point:** register

---

## 5. Inputs

Workflow accepts input payload matching CC_REGISTER_NAME_V0 input contract:

| Field | Type | Required |
|-------|------|----------|
| name | string | yes |
| resource_addresses | array | yes |

---

## 6. Outputs

Workflow returns output matching CC_REGISTER_NAME_V0 output contract:

| Field | Type | Required |
|-------|------|----------|
| success | boolean | yes |

---

## Machine

```yaml
wf_code: WF_REGISTER_NAME_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: pgs_capabilities.registry.name_service.runtime_bindings::RB_NAME_SERVICE_V0

core:
  summary: Register or update name-to-resource-addresses mapping

  start_node: entry

  nodes:
    entry:
      type: IN
      next:
        default: register

    register:
      type: CC
      code: pgs_capabilities.registry.name_service.capability_contracts::CC_REGISTER_NAME_V0
      next:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

    exit:
      type: EXIT

  entry: entry
  exit: exit
```
