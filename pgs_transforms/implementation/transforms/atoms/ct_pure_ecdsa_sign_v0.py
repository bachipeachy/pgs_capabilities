"""
CT_PURE_ECDSA_SIGN_V0

Pure Capability Transform (Atom)

Purpose:
    Sign a message hash using ECDSA with a specified curve.

Implementation:
    - Uses coincurve for secp256k1 signing
    - Produces recoverable signature (v, r, s) components
    - Returns signed_bytes as hex string
"""

from typing import Dict, Any
from coincurve import PrivateKey


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "private_key_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_ECDSA_SIGN_V0: missing required input 'private_key_bytes'"
        )
    if "message_hash" not in inputs:
        raise ValueError(
            "CT_PURE_ECDSA_SIGN_V0: missing required input 'message_hash'"
        )

    curve = inputs.get("curve", "secp256k1")

    if curve != "secp256k1":
        raise ValueError(
            f"CT_PURE_ECDSA_SIGN_V0: unsupported curve '{curve}'. Only 'secp256k1' is supported in V0."
        )

    # Atom canonicalizes hex_string inputs to bytes
    private_key_bytes = inputs["private_key_bytes"]

    if isinstance(private_key_bytes, str):
        hex_str = private_key_bytes[2:] if private_key_bytes.startswith("0x") else private_key_bytes
        private_key_bytes = bytes.fromhex(hex_str)

    if len(private_key_bytes) != 32:
        raise ValueError(
            f"CT_PURE_ECDSA_SIGN_V0: private_key_bytes must be 32 bytes, got {len(private_key_bytes)}"
        )

    # Atom canonicalizes hex_string inputs to bytes
    message_hash_bytes = inputs["message_hash"]

    if isinstance(message_hash_bytes, str):
        hex_str = message_hash_bytes[2:] if message_hash_bytes.startswith("0x") else message_hash_bytes
        message_hash_bytes = bytes.fromhex(hex_str)

    if len(message_hash_bytes) != 32:
        raise ValueError(
            f"CT_PURE_ECDSA_SIGN_V0: message_hash must be 32 bytes, got {len(message_hash_bytes)}"
        )

    # Sign with recoverable signature
    key = PrivateKey(private_key_bytes)
    signature = key.sign_recoverable(message_hash_bytes, hasher=None)

    # coincurve returns 65 bytes: r (32) + s (32) + recovery_id (1)
    r = signature[:32]
    s = signature[32:64]
    v = signature[64]

    # Build signed_bytes: the full 65-byte recoverable signature as hex
    signed_bytes_hex = "0x" + signature.hex()

    return {
        "v": v,
        "r": "0x" + r.hex(),
        "s": "0x" + s.hex(),
        "signed_bytes": signed_bytes_hex
    }
