# CC_LOOKUP_NAME_V0

## Header

- **Artifact Code:** CC_LOOKUP_NAME_V0
- **Artifact Kind:** capability_contract
- **Governed By:** fb.constitution::CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:** pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0

---

## 1. Intent

Look up resource addresses for a given name via name service.

---

## 2. Operation

READ

---

## 3. Bindings

- **Target:** pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Name to look up (e.g., alice@example.com) |

---

## 5. Outputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource_addresses | array | yes | List of resource addresses for this name |

**Note:** Output MUST include `resource_addresses` field even if empty array.

---

## 6. Contract

**Input Contract:**
- `name` is required and must be string
- Empty name is invalid (handled by CS)

**Output Contract:**
- MUST return `resource_addresses` field
- Type MUST be array of strings
- Empty array if name not found

**Result Status:**
- SUCCESS: Name found, addresses returned
- NOT_FOUND: Name not registered
- VIOLATION: Invalid input
- BACKEND_ERROR: Storage failure

---

## Machine

```yaml
cc_code: CC_LOOKUP_NAME_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: Look up resource addresses for a given name

  inputs:
    name:
      type: string
      required: true
      description: Name to look up (e.g., alice@example.com)

  outputs:
    resource_addresses:
      type: array
      items:
        type: string
      required: true
      description: List of resource addresses for this name

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]

  pipeline:
    - step: lookup
      side_effect: pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0
      op: READ
      inputs:
        name: $.inputs.name
      outputs:
        resource_addresses: $.capability_result.value.resource_addresses
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
