# CT_PURE_LOOKUP_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_LOOKUP_V0
- **Artifact Kind:** capability_transform
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Machine

```yaml
ct_code: CT_PURE_LOOKUP_V0
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Look up key in map
  description: Returns the value associated with a key from a provided key-value mapping object.
  
  inputs:
    key:
      type: string
      required: true
      description: The key to look for
    map:
      type: object
      required: true
      description: The mapping object to search in

  outputs:
    result:
      type: any
      required: true
      description: The value found for the given key

machine:
  ct_kind: atom
  ct_purity: ct_pure
  implementation:
    module: pgs_transforms.implementation.transforms.atoms.ct_pure_lookup_v0
    callable: execute
```
