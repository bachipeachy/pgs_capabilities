"""
CT_PURE_GENERATE_ENTROPY_V0

Pure Capability Transform (Atom)

Purpose:
    Generate cryptographically secure entropy bytes of a specified strength.

Notes:
    - This atom intentionally encapsulates NON-determinism.
    - No state, no caching, no side effects.
    - Entropy source is OS-provided CSPRNG.
    - Behavior is extracted verbatim from existing crypto implementation
      (hd_wallet.generate_mnemonic).
"""

import os
from typing import Dict, Any


# Allowed entropy strengths (bits), aligned with existing crypto rules
_ALLOWED_ENTROPY_BITS = {128, 160, 192, 224, 256}


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Execute CT_PURE_GENERATE_ENTROPY_V0.

    Inputs:
        entropy_bits (int): One of {128, 160, 192, 224, 256}

    Outputs:
        entropy_bytes (bytes): Cryptographically secure random bytes
    """

    # ---- Fail-loud input validation ----
    if "entropy_bits" not in inputs:
        raise ValueError("CT_PURE_GENERATE_ENTROPY_V0: missing required input 'entropy_bits'")

    entropy_bits = inputs["entropy_bits"]

    if not isinstance(entropy_bits, int):
        raise TypeError(
            f"CT_PURE_GENERATE_ENTROPY_V0: entropy_bits must be int, got {type(entropy_bits).__name__}"
        )

    if entropy_bits not in _ALLOWED_ENTROPY_BITS:
        raise ValueError(
            f"CT_PURE_GENERATE_ENTROPY_V0: entropy_bits must be one of "
            f"{sorted(_ALLOWED_ENTROPY_BITS)}, got {entropy_bits}"
        )

    # ---- Core entropy generation (no rewrite, no extras) ----
    entropy_len_bytes = entropy_bits // 8
    entropy_bytes = os.urandom(entropy_len_bytes)

    # ---- Defensive sanity check ----
    if not isinstance(entropy_bytes, (bytes, bytearray)):
        raise RuntimeError(
            "CT_PURE_GENERATE_ENTROPY_V0: entropy source returned invalid type"
        )

    if len(entropy_bytes) != entropy_len_bytes:
        raise RuntimeError(
            "CT_PURE_GENERATE_ENTROPY_V0: entropy length mismatch "
            f"(expected {entropy_len_bytes}, got {len(entropy_bytes)})"
        )

    # Return hex_string to match contract output type
    # Guard against already-converted values
    if isinstance(entropy_bytes, bytes):
        entropy_bytes = "0x" + entropy_bytes.hex()

    return {
        "entropy_bytes": entropy_bytes
    }
