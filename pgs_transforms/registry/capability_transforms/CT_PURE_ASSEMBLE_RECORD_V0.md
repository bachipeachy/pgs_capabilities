# CT_PURE_ASSEMBLE_RECORD_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_ASSEMBLE_RECORD_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Machine

```yaml
ct_code: CT_PURE_ASSEMBLE_RECORD_V0
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Assemble record object
  description: Combines multiple input values into a single structured record object.
  
  inputs:
    fields:
      type: object
      required: true
      description: Key-value map of fields to include in the record

  outputs:
    record:
      type: object
      required: true
      description: The assembled record object

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: ASSEMBLE_RECORD
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_assemble_record_v0
    callable: execute
```
