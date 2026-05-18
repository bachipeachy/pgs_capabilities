"""
CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0

Pure Capability Transform (Atom)

Purpose:
    Derive an uncompressed public key from a private key scalar on a specified elliptic curve.

Implementation:
    - Uses cryptography.hazmat.primitives.asymmetric.ec
    - Supports secp256k1 and secp256r1
    - Enforces scalar validity (0 < k < order)
    - Returns uncompressed point (0x04 || X || Y)
"""

from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "private_key_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0: missing required input 'private_key_bytes'"
        )
    if "curve" not in inputs:
        raise ValueError(
            "CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0: missing required input 'curve'"
        )

    # Atom canonicalizes hex_string inputs to bytes
    private_key_bytes = inputs["private_key_bytes"]
    curve_name = inputs["curve"]

    if isinstance(private_key_bytes, str):
        hex_str = private_key_bytes[2:] if private_key_bytes.startswith("0x") else private_key_bytes
        private_key_bytes = bytes.fromhex(hex_str)

    if not isinstance(curve_name, str):
        raise TypeError(
            "CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0: curve must be a string"
        )
    
    # Inline curve selection
    if curve_name == "secp256k1":
        curve = ec.SECP256K1()
    elif curve_name == "secp256r1":
        curve = ec.SECP256R1()
    else:
        raise ValueError(
            f"CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0: unsupported curve '{curve_name}'"
        )

    # Inline derivation
    try:
        private_key = ec.derive_private_key(
            int.from_bytes(private_key_bytes, byteorder="big"),
            curve,
            default_backend()
        )
    except ValueError as e:
        raise ValueError("CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0: Invalid private key for the specified curve.") from e

    public_key = private_key.public_key()
    
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # Return hex_string to match contract output type
    # Guard against already-converted values
    if isinstance(public_key_bytes, bytes):
        public_key_bytes = "0x" + public_key_bytes.hex()

    return {
        "public_key_uncompressed_bytes": public_key_bytes
    }
