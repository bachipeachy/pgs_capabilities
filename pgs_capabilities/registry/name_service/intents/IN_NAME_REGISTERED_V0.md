# IN_NAME_REGISTERED_V0

## Header (Mandatory)

- **Artifact Code:** IN_NAME_REGISTERED_V0
- **Artifact Kind:** intent
- **Governed By:** fb.topology::CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** pgs_capabilities.registry.name_service.workflows::WF_REGISTER_NAME_V0

---

## 1. Intent

Request to register or update a name-to-resource-addresses mapping in the name registry.

---

## 2. Rationale

Name registration intent is a protocol entry point:
- Declares desired outcome (name is registered/updated)
- Protocol validates and persists mapping
- Outcome is deterministic (SUCCESS or FAILURE)

This enables:
- External invocation via transport layer (HTTP, message queue, etc.)
- Internal invocation from other workflows
- Consistent entry point regardless of invocation source

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_REGISTER_NAME_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | true | Human-readable name (e.g., email address) |
| resource_addresses | array | true | List of resource addresses to associate with name |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Registration request accepted for processing |
| NACK | Registration request rejected (validation failure) |

---

## Machine

```yaml
in_code: IN_NAME_REGISTERED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Register or update name-to-resource-addresses mapping
  workflow: pgs_capabilities.registry.name_service.workflows::WF_REGISTER_NAME_V0

  inputs:
    name:
      type: string
      required: true
      description: Human-readable name (e.g., email address)

    resource_addresses:
      type: array
      required: true
      description: List of resource addresses to associate with name

  outcomes:
    ACK:
      description: Registration request accepted for processing
    NACK:
      description: Registration request rejected (validation failure)
```
