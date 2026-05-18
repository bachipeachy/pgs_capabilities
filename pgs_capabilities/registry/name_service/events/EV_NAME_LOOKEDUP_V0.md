# EV_NAME_LOOKEDUP_V0

## Header (Mandatory)

- **Artifact Code:** EV_NAME_LOOKEDUP_V0
- **Artifact Kind:** event
- **Governed By:** fb.constitution::CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A name lookup was performed in the name registry.

---

## 2. Rationale

Name lookup is a protocol-governed query operation:
- Resolves human-readable names to resource addresses
- Records lookup requests for audit trail
- Supports diagnostics and usage analytics
- Distinguishes between found and not-found outcomes

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_LOOKUP_NAME_V0 | CC_LOOKUP_NAME_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | true | Human-readable name that was looked up |
| resource_addresses | array | false | Resource addresses if name was found (empty if not found) |
| found | boolean | true | Whether the name was found in registry |
| timestamp | string (date-time) | true | When lookup occurred |

---

## Machine

```yaml
ev_code: EV_NAME_LOOKEDUP_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Name Looked Up
  description: Emitted when a name lookup is performed

  schema:
    name:
      type: string
      required: true
      description: Human-readable name that was looked up
    resource_addresses:
      type: array
      required: false
      description: Resource addresses if name was found
    found:
      type: boolean
      required: true
      description: Whether the name was found in registry
    timestamp:
      type: string
      format: date-time
      required: true
      description: When lookup occurred
```
