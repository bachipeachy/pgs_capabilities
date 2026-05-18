# IN_NAME_LOOKEDUP_V0

## Header (Mandatory)

- **Artifact Code:** IN_NAME_LOOKEDUP_V0
- **Artifact Kind:** intent
- **Governed By:** fb.topology::CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** pgs_capabilities.registry.name_service.workflows::WF_LOOKUP_NAME_V0

---

## 1. Intent

Request to lookup resource addresses associated with a registered name.

---

## 2. Rationale

Name lookup intent is a protocol entry point:
- Declares desired outcome (retrieve addresses for name)
- Protocol queries registry and returns results
- Outcome is deterministic (FOUND or NOT_FOUND)

This enables:
- External invocation via transport layer (HTTP, message queue, etc.)
- Internal invocation from other workflows
- Consistent entry point regardless of invocation source

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_LOOKUP_NAME_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | true | Human-readable name to lookup (e.g., email address) |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Lookup request accepted for processing |
| NACK | Lookup request rejected (validation failure) |

---

## Machine

```yaml
in_code: IN_NAME_LOOKEDUP_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Lookup resource addresses for a registered name
  workflow: pgs_capabilities.registry.name_service.workflows::WF_LOOKUP_NAME_V0

  inputs:
    name:
      type: string
      required: true
      description: Human-readable name to lookup (e.g., email address)

  outcomes:
    ACK:
      description: Lookup request accepted for processing
    NACK:
      description: Lookup request rejected (validation failure)
```
