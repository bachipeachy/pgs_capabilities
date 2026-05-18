# RB_NAME_SERVICE_V0

## Header

- **Artifact Code:** RB_NAME_SERVICE_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** fb.topology::CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Dependencies:**
  - pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0

---

## 1. Purpose

Bind name service capability to its runtime implementation. Provides configuration for persistent storage of name-to-resource-address mappings.

---

## 2. Bindings

| CS Code | Type | Configuration |
|---------|------|---------------|
| CS_NAME_REGISTRY_V0 | CS | path: {{module_data_root}}/name_registry.json |

**Note:** Runtime resolves CS implementation. Protocol only declares type and config.

---

## 3. Parameters

- `module_data_root` — base path for module data storage

---

## Machine

```yaml
rb_code: RB_NAME_SERVICE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

parameters:
  - module_data_root

core:
  summary: Bind name service capability to runtime implementation

  bindings:
    pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0:
      type: CS
      config:
        path: "{{module_data_root}}/name_registry.json"
```
