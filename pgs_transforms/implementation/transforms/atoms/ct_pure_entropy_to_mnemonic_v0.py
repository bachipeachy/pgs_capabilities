"""
CT_PURE_ENTROPY_TO_MNEMONIC_V0

Pure Capability Transform (Atom)

Purpose:
    Convert raw entropy bytes into a BIP-39 mnemonic phrase.

Implementation:
    - Uses bip_utils.Bip39MnemonicGenerator
    - Validates entropy length (128-256 bits)
    - Returns string mnemonic
"""

from typing import Dict, Any
from bip_utils import Bip39MnemonicGenerator, Bip39Languages


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "entropy_bytes" not in inputs:
        raise ValueError(
            "CT_PURE_ENTROPY_TO_MNEMONIC_V0: missing required input 'entropy_bytes'"
        )

    # Atom canonicalizes hex_string inputs to bytes
    entropy_bytes = inputs["entropy_bytes"]

    if isinstance(entropy_bytes, str):
        hex_str = entropy_bytes[2:] if entropy_bytes.startswith("0x") else entropy_bytes
        entropy_bytes = bytes.fromhex(hex_str)

    strength_bits = len(entropy_bytes) * 8
    if strength_bits not in (128, 160, 192, 224, 256):
        raise ValueError(
            f"CT_PURE_ENTROPY_TO_MNEMONIC_V0: invalid entropy length: {strength_bits} bits"
        )

    # Inline implementation using bip_utils directly
    mnemonic_obj = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromEntropy(bytes(entropy_bytes))
    mnemonic = mnemonic_obj.ToStr()

    return {
        "mnemonic": mnemonic
    }
