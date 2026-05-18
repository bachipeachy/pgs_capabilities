"""
CT_PURE_KECCAK256_HASH_V0

Pure Capability Transform (Atom)

Purpose:
    Compute the Keccak-256 hash of arbitrary input bytes.

Implementation:
    - Uses Crypto.Hash.keccak (pycryptodome)
    - Input is a hex string (with or without 0x prefix)
    - Returns 0x-prefixed hex hash string
"""

from typing import Dict, Any
from Crypto.Hash import keccak


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "input_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_KECCAK256_HASH_V0: missing required input 'input_bytes'"
        )

    input_bytes = inputs["input_bytes"]

    if isinstance(input_bytes, str):
        hex_str = input_bytes
        if hex_str.startswith("0x") or hex_str.startswith("0X"):
            hex_str = hex_str[2:]
        try:
            raw_bytes = bytes.fromhex(hex_str)
        except ValueError as e:
            raise ValueError(
                f"CT_PURE_KECCAK256_HASH_V0: invalid hex string: {e}"
            )
    elif isinstance(input_bytes, (bytes, bytearray)):
        raw_bytes = bytes(input_bytes)
    else:
        raise TypeError(
            f"CT_PURE_KECCAK256_HASH_V0: input_bytes must be hex string or bytes, got {type(input_bytes).__name__}"
        )

    k = keccak.new(digest_bits=256)
    k.update(raw_bytes)
    hash_hex = "0x" + k.hexdigest()

    return {
        "hash_hex": hash_hex
    }
