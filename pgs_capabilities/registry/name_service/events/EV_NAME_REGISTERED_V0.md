# EV_NAME_REGISTERED_V0

## Header (Mandatory)

- **Artifact Code:** EV_NAME_REGISTERED_V0
- **Artifact Kind:** event
- **Governed By:** fb.constitution::CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A name-to-resource-addresses mapping has been successfully registered or updated in the name registry.

---

## 2. Rationale

Name registration is a protocol-governed state transition:
- Records human-readable name to resource address mapping
- Enables name-based resource discovery
- Provides audit trail for name ownership
- Supports name updates and conflict resolution

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_REGISTER_NAME_V0 | CC_REGISTER_NAME_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | true | Human-readable name that was registered |
| resource_addresses | array | true | Resource addresses associated with the name |
| success | boolean | true | Whether registration succeeded |
| timestamp | string (date-time) | true | When registration occurred |

---

## Machine

```yaml
ev_code: EV_NAME_REGISTERED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Name Registered
  description: Emitted when a name-to-resource-addresses mapping is registered or updated

  schema:
    name:
      type: string
      required: true
      description: Human-readable name that was registered
    resource_addresses:
      type: array
      required: true
      description: Resource addresses associated with the name
    success:
      type: boolean
      required: true
      description: Whether registration succeeded
    timestamp:
      type: string
      format: date-time
      required: true
      description: When registration occurred
```
