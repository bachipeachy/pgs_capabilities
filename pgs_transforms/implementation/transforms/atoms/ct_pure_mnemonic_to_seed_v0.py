"""
CT_PURE_MNEMONIC_TO_SEED_V0

Pure Capability Transform (Atom)

Purpose:
    Convert a BIP-39 mnemonic phrase into a binary seed using PBKDF2.

Implementation:
    - Uses bip_utils.Bip39SeedGenerator
    - Validates mnemonic format
    - Supports optional passphrase
"""

from typing import Dict, Any
from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip39Languages


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "mnemonic" not in inputs:
        raise ValueError(
            "CT_PURE_MNEMONIC_TO_SEED_V0: missing required input 'mnemonic'"
        )

    mnemonic = inputs["mnemonic"]
    passphrase = inputs.get("passphrase", "")

    if not isinstance(mnemonic, str):
        raise TypeError(
            "CT_PURE_MNEMONIC_TO_SEED_V0: mnemonic must be a string"
        )

    # Inline validation
    if not Bip39MnemonicValidator(Bip39Languages.ENGLISH).IsValid(mnemonic):
        raise ValueError("CT_PURE_MNEMONIC_TO_SEED_V0: Invalid BIP-39 mnemonic provided.")

    # Inline seed generation
    seed_bytes = Bip39SeedGenerator(mnemonic, Bip39Languages.ENGLISH).Generate(passphrase)

    # Ensure bytes type
    seed_bytes = bytes(seed_bytes)

    # Return hex_string to match contract output type
    # Guard against already-converted values
    if isinstance(seed_bytes, bytes):
        seed_bytes = "0x" + seed_bytes.hex()

    return {
        "seed_bytes": seed_bytes
    }
