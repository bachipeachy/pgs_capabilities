"""
CT_PURE_GENERATE_ID_V0

Pure Capability Transform (Atom)

Purpose:
    Generate deterministic IDs from structured data.
    This is the ONLY mechanism for identity creation within the protocol.

Implementation:
    - Canonicalize data via sorted JSON
    - SHA256 hash
    - Prefix result
    - PURE: No timestamps, no execution context, no side channels
"""

from typing import Dict, Any
import json
import hashlib


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Generate a deterministic ID.

    Args:
        inputs: {
            "prefix": str - ID prefix (e.g., "KYC", "WALLET")
            "data": dict - Data to hash (will be canonicalized)
        }

    Returns:
        {
            "value": str - Generated ID (prefix_hash)
        }
    """
    # Validate inputs
    if "prefix" not in inputs:
        raise ValueError("CT_PURE_GENERATE_ID_V0: missing required input 'prefix'")
    if "data" not in inputs:
        raise ValueError("CT_PURE_GENERATE_ID_V0: missing required input 'data'")

    prefix = inputs["prefix"]
    data = inputs["data"]

    if not isinstance(prefix, str):
        raise TypeError(
            f"CT_PURE_GENERATE_ID_V0: prefix must be string, got {type(prefix).__name__}"
        )

    # Canonicalize data to dict for deterministic hashing
    # Contract allows type: any, so handle all primitive types
    if isinstance(data, dict):
        # Already a dict - use directly
        canonical_data = data
    else:
        # Primitive type (string, number, etc.) - wrap in consistent structure
        canonical_data = {"value": data}

    # Generate deterministic ID
    result = generate_deterministic_id(prefix=prefix, content=canonical_data)

    return {"id": result}


def generate_deterministic_id(prefix: str, content: dict) -> str:
    """
    Generate a deterministic ID from content.

    Canonical JSON serialization ensures same content → same ID.
    """
    # Canonical JSON (sorted keys, no whitespace)
    canonical = json.dumps(content, sort_keys=True, separators=(",", ":"))

    # SHA256 hash
    hash_bytes = hashlib.sha256(canonical.encode("utf-8")).digest()
    hash_hex = hash_bytes.hex()

    # Prefix + first 16 chars of hash
    return f"{prefix}_{hash_hex[:16]}"
