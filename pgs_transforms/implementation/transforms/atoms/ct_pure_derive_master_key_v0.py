"""
CT_PURE_DERIVE_MASTER_KEY_V0

Pure Capability Transform (Atom)

Purpose:
    Derive a BIP-32 master private key and chain code from a seed.

Implementation:
    - Uses bip_utils.Bip32Secp256k1
    - Validates seed length
    - Returns raw bytes for key and chain code
"""

from typing import Dict, Any
from bip_utils import Bip32Secp256k1


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "seed_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_DERIVE_MASTER_KEY_V0: missing required input 'seed_bytes'"
        )

    # Atom canonicalizes hex_string inputs to bytes
    seed_bytes = inputs["seed_bytes"]

    if isinstance(seed_bytes, str):
        hex_str = seed_bytes[2:] if seed_bytes.startswith("0x") else seed_bytes
        seed_bytes = bytes.fromhex(hex_str)

    if len(seed_bytes) < 16: # 128 bits
         raise ValueError(
            "CT_PURE_DERIVE_MASTER_KEY_V0: seed_bytes length must be at least 128 bits"
        )

    # Inline derivation
    bip32_mst = Bip32Secp256k1.FromSeed(seed_bytes)

    master_private_key = bip32_mst.PrivateKey().Raw().ToBytes()
    master_chain_code = bip32_mst.ChainCode().ToBytes()

    # Return hex_string to match contract output type
    # Guard against already-converted values
    if isinstance(master_private_key, bytes):
        master_private_key = "0x" + master_private_key.hex()
    if isinstance(master_chain_code, bytes):
        master_chain_code = "0x" + master_chain_code.hex()

    return {
        "master_private_key_bytes": master_private_key,
        "master_chain_code_bytes": master_chain_code
    }
