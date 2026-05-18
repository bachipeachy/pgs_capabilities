"""
utils.py — Low-level helpers for CS_MUTABLE_JSON_V0.
"""

import json
import os
import tempfile
from typing import Any, Dict


def validate_key(key: Any) -> bool:
    """
    Validate key semantics.
    Keys must be non-empty strings.
    """
    return isinstance(key, str) and bool(key.strip())


def atomic_write_json(path: str | os.PathLike, data: Dict[str, Any]) -> None:
    """
    Atomically write JSON data to disk.
    Write to temp file, fsync, then replace.
    """
    path_str = os.fspath(path)  # ← canonical normalization
    directory = os.path.dirname(path_str) or "."

    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_path, path_str)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
