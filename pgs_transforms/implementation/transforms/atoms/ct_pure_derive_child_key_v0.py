"""
CT_PURE_DERIVE_CHILD_KEY_V0

Pure Capability Transform (Atom)

Purpose:
    Derive a single BIP-32 child private key and chain code from a parent key.

Implementation:
    - Uses bip_utils.Bip32Secp256k1
    - Reconstructs parent context from raw bytes
    - Derives child at index
    - Returns raw bytes
"""

from typing import Dict, Any
from bip_utils import (
    Bip32Secp256k1,
    Bip32KeyData,
    Bip32ChainCode,
    Bip32Depth,
    Bip32KeyIndex,
    Bip32FingerPrint
)


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "parent_private_key_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_DERIVE_CHILD_KEY_V0: missing required input 'parent_private_key_bytes'"
        )
    if "parent_chain_code_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_DERIVE_CHILD_KEY_V0: missing required input 'parent_chain_code_bytes'"
        )
    if "index" not in inputs:
        raise ValueError(
            "CT_PURE_DERIVE_CHILD_KEY_V0: missing required input 'index'"
        )

    # Atom canonicalizes hex_string inputs to bytes
    parent_private_key = inputs["parent_private_key_bytes"]
    parent_chain_code = inputs["parent_chain_code_bytes"]
    index = inputs["index"]

    # Canonicalize hex_string to bytes
    if isinstance(parent_private_key, str):
        hex_str = parent_private_key[2:] if parent_private_key.startswith("0x") else parent_private_key
        parent_private_key = bytes.fromhex(hex_str)

    if isinstance(parent_chain_code, str):
        hex_str = parent_chain_code[2:] if parent_chain_code.startswith("0x") else parent_chain_code
        parent_chain_code = bytes.fromhex(hex_str)

    if not isinstance(index, int):
        raise TypeError(
            "CT_PURE_DERIVE_CHILD_KEY_V0: index must be an integer"
        )

    if len(parent_private_key) != 32:
        raise ValueError(
            "CT_PURE_DERIVE_CHILD_KEY_V0: parent_private_key_bytes must be 32 bytes"
        )
    if len(parent_chain_code) != 32:
        raise ValueError(
            "CT_PURE_DERIVE_CHILD_KEY_V0: parent_chain_code_bytes must be 32 bytes"
        )
        
    if index < 0 or index > 0xFFFFFFFF:
        raise ValueError(
            "CT_PURE_DERIVE_CHILD_KEY_V0: index must be a 32-bit unsigned integer"
        )

    # Inline derivation
    # Reconstruct the Bip32 object from the parent key and chain code
    # We must wrap the chain code in Bip32KeyData to satisfy bip_utils requirements
    key_data = Bip32KeyData(
        depth=Bip32Depth(0),
        index=Bip32KeyIndex(0),
        parent_fprint=Bip32FingerPrint(),
        chain_code=Bip32ChainCode(bytes(parent_chain_code)),
    )
    
    bip32_parent = Bip32Secp256k1.FromPrivateKey(bytes(parent_private_key), key_data)
    
    # Derive the child
    bip32_child = bip32_parent.ChildKey(index)

    child_private_key = bip32_child.PrivateKey().Raw().ToBytes()
    child_chain_code = bip32_child.ChainCode().ToBytes()

    # Return hex_string to match contract output type
    # Guard against already-converted values
    if isinstance(child_private_key, bytes):
        child_private_key = "0x" + child_private_key.hex()
    if isinstance(child_chain_code, bytes):
        child_chain_code = "0x" + child_chain_code.hex()

    return {
        "child_private_key_bytes": child_private_key,
        "child_chain_code_bytes": child_chain_code
    }
