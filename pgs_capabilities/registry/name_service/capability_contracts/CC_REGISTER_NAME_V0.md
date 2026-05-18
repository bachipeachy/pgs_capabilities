# CC_REGISTER_NAME_V0

## Header

- **Artifact Code:** CC_REGISTER_NAME_V0
- **Artifact Kind:** capability_contract
- **Governed By:** fb.constitution::CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:** pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0

---

## 1. Intent

Register or update name-to-resource-addresses mapping via name service.

---

## 2. Operation

WRITE

---

## 3. Bindings

- **Target:** pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Name to register (e.g., alice@example.com) |
| resource_addresses | array | yes | List of resource addresses to map to this name |

---

## 5. Outputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| success | boolean | yes | True if registration succeeded |

**Note:** Output MUST include `success` field.

---

## 6. Contract

**Input Contract:**
- `name` is required and must be string
- `resource_addresses` is required and must be array of strings
- Empty name is invalid (handled by CS)
- Empty addresses array is allowed (clears mapping)

**Output Contract:**
- MUST return `success` field
- Type MUST be boolean
- `true` on SUCCESS status
- `false` on non-SUCCESS status

**Result Status:**
- SUCCESS: Name registered/updated successfully
- VIOLATION: Invalid input (empty name, wrong types)
- BACKEND_ERROR: Storage failure

---

## Machine

```yaml
cc_code: CC_REGISTER_NAME_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: Register or update name-to-resource-addresses mapping

  inputs:
    name:
      type: string
      required: true
      description: Name to register (e.g., alice@example.com)
    resource_addresses:
      type: array
      items:
        type: string
      required: true
      description: List of resource addresses to map to this name

  outputs:
    success:
      type: boolean
      required: true
      description: True if registration succeeded

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]

  pipeline:
    - step: register
      side_effect: pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0
      op: WRITE
      inputs:
        name: $.inputs.name
        resource_addresses: $.inputs.resource_addresses
      outputs:
        success: $.capability_result.value.success
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
