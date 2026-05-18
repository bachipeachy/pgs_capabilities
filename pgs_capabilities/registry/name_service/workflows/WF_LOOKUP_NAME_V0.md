# WF_LOOKUP_NAME_V0

## Header

- **Artifact Code:** WF_LOOKUP_NAME_V0
- **Artifact Kind:** workflow
- **Governed By:** fb.topology::CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:** pgs_capabilities.registry.name_service.capability_contracts::CC_LOOKUP_NAME_V0

---

## 1. Intent

Look up resource addresses for a given name via protocol path.

---

## 2. Flow

```
entry → lookup → exit
```

Single-step workflow that invokes name lookup capability contract.

---

## 3. Steps

### Step: lookup

- **Uses:** pgs_capabilities.registry.name_service.capability_contracts::CC_LOOKUP_NAME_V0
- **Operation:** READ
- **Role:** Look up name and return resource addresses

---

## 4. Entry and Exit

- **Entry Point:** lookup
- **Exit Point:** lookup

---

## 5. Inputs

Workflow accepts input payload matching CC_LOOKUP_NAME_V0 input contract:

| Field | Type | Required |
|-------|------|----------|
| name | string | yes |

---

## 6. Outputs

Workflow returns output matching CC_LOOKUP_NAME_V0 output contract:

| Field | Type | Required |
|-------|------|----------|
| resource_addresses | array | yes |

---

## Machine

```yaml
wf_code: WF_LOOKUP_NAME_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: pgs_capabilities.registry.name_service.runtime_bindings::RB_NAME_SERVICE_V0

core:
  summary: Look up resource addresses for a given name

  start_node: entry

  nodes:
    entry:
      type: IN
      next:
        default: lookup

    lookup:
      type: CC
      code: pgs_capabilities.registry.name_service.capability_contracts::CC_LOOKUP_NAME_V0
      next:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

    exit:
      type: EXIT

  entry: entry
  exit: exit
```
