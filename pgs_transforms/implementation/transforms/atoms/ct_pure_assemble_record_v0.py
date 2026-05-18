"""
CT_PURE_ASSEMBLE_RECORD_V0

Pure Capability Transform (Atom)

Assembles arbitrary named inputs into a single output record.
"""

from typing import Dict, Any


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Assemble a record from input fields.

    According to CT contract:
    - Input: fields (object) - key-value map of fields to include
    - Output: record (object) - the assembled record containing those fields directly

    Implementation: If 'fields' object provided, use it. Otherwise, assemble all inputs into record.
    """
    if "fields" in inputs:
        # Contract-compliant: fields object provided
        fields = inputs["fields"]
    else:
        # Molecule calling pattern: all inputs are fields
        fields = dict(inputs)

    return {
        "record": fields
    }
