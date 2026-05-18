"""
CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0

Pure Capability Transform (Atom)

Purpose:
    Derive an Ethereum address from an uncompressed public key.

Implementation:
    - Uses Crypto.Hash.keccak (pycryptodome)
    - Validates public key format (65 bytes, 0x04 prefix)
    - Returns 0x-prefixed hex string
"""

from typing import Dict, Any
from Crypto.Hash import keccak


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "public_key_uncompressed_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0: missing required input 'public_key_uncompressed_bytes'"
        )

    # Atom canonicalizes hex_string inputs to bytes
    public_key_bytes = inputs["public_key_uncompressed_bytes"]

    if isinstance(public_key_bytes, str):
        hex_str = public_key_bytes[2:] if public_key_bytes.startswith("0x") else public_key_bytes
        public_key_bytes = bytes.fromhex(hex_str)

    # Inline validation
    if len(public_key_bytes) != 65:
        raise ValueError(f"CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0: Invalid public key length: {len(public_key_bytes)} bytes. Expected 65 bytes.")
        
    if public_key_bytes[0] != 0x04:
        raise ValueError(f"CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0: Invalid public key prefix: {hex(public_key_bytes[0])}. Expected 0x04.")

    # Inline derivation
    # 1. Drop the 0x04 prefix
    raw_pub_key = public_key_bytes[1:]
    
    # 2. Keccak-256 hash
    k = keccak.new(digest_bits=256)
    k.update(raw_pub_key)
    hashed_key = k.digest()
    
    # 3. Take the last 20 bytes
    address_bytes = hashed_key[-20:]
    
    # 4. Format as hex string
    eth_address = "0x" + address_bytes.hex()

    return {
        "eth_address_hex": eth_address
    }
