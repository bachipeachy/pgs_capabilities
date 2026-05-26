# CS_SEND_EMAIL_V0

## Header (Mandatory)

- **Artifact Code:** CS_SEND_EMAIL_V0
- **Artifact Kind:** capability_side_effect
- **Governed By:** CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Send email notifications via SMTP. Testbed-safe: skips gracefully when SMTP is not configured.

---

## 2. Rationale

Email notification side-effect:
- Provides non-structural notification capability for workflow events
- Best-effort delivery — failure does not cascade to workflow failure
- Testbed-safe: returns SUCCESS with `delivery_status: "skipped"` when SMTP env vars are absent
- No persistence — sent emails are not stored by this CS

---

## 3. Applicability

- Post-action notifications (wallet created, actor verified)
- Any workflow step requiring best-effort email delivery

---

## 4. Non-Applicability

- Transactional email requiring delivery guarantees
- Email templates requiring rich HTML rendering
- Bulk email or marketing campaigns

---

## 5. Side-Effect Category

| Property | Value |
|----------|-------|
| Type | external |
| Durability | none |
| Idempotent | false |
| Replay Policy | no_replay |

---

## 6. Operations

### SEND

Send a single email to a recipient.

**Inputs:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| recipient | string | true | Recipient email address |
| subject | string | false | Email subject line |
| body_template | string | false | Template name for email body |
| template_vars | object | false | Variables to interpolate into template |

**Outputs:**
| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |
| delivery_status | string | "sent" or "skipped" |

**Result Statuses:**
| Status | Condition |
|--------|-----------|
| SUCCESS | Email sent or skipped (SMTP not configured) |
| VIOLATION | Invalid recipient email address |
| BACKEND_ERROR | SMTP connection or authentication failure |

---

## 7. Failure Semantics

- Missing or invalid recipient: VIOLATION
- SMTP not configured: SUCCESS with `delivery_status: "skipped"` (testbed-safe)
- SMTP connection failure: BACKEND_ERROR (non-structural, does not fail workflow)

---

## 8. Configuration Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| smtp_host | string | false | SMTP server hostname (falls back to SMTP_HOST env var) |
| smtp_port | integer | false | SMTP server port (default 587) |
| smtp_user | string | false | SMTP authentication username |
| smtp_pass | string | false | SMTP authentication password |
| sender | string | false | Sender email address (default noreply@pgs.local) |

---

## Machine

```yaml
cs_code: CS_SEND_EMAIL_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: SMTP email sending with testbed-safe skipping
  side_effect_type: external
  durability: none
  idempotent: false

  policy:
    operations: [SEND]

  operations:
    SEND:
      summary: Send email via SMTP
      handler: send
      input: [to, subject, body]
      output: [result_status]
      idempotent: false

  configuration:
    smtp_host:
      type: string
      required: false
    smtp_port:
      type: integer
      required: false
    smtp_user:
      type: string
      required: false
    smtp_pass:
      type: string
      required: false
    sender:
      type: string
      required: false

implementation:
  module: pgs_side_effects.implementation.side_effects.external.CS_SEND_EMAIL_V0.runtime
  callable: SendEmailRuntime
```
