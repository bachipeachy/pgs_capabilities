"""
executor.py — Capability semantics for CS_APPENDONLY_JSONL_V0.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class AppendOnlyJsonlEngine:
    """Append-only JSONL storage with sequence numbering."""

    def __init__(self, config: Dict[str, Any]):
        self._path = Path(config["path"])
        self._sequence_counter = 0
        if self._path.exists():
            with open(self._path) as f:
                self._sequence_counter = sum(1 for _ in f)

    def append(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Append a record to the log."""
        record = payload.get("record")
        stream_id = payload.get("stream_id")
        actor_id = payload.get("actor_id")

        timestamp = datetime.utcnow().isoformat()
        record_id = f"{timestamp}_{self._sequence_counter:06d}"
        self._sequence_counter += 1
        sequence_number = self._sequence_counter

        log_entry = {
            "record_id": record_id,
            "sequence_number": sequence_number,
            "timestamp": timestamp,
            "actor_id": actor_id,
            "stream_id": stream_id,
            "record": record,
        }

        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {
            "result_status": "SUCCESS",
            "record_id": record_id,
            "sequence_number": sequence_number,
        }

    def read_all(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Read all entries from the log, optionally filtered by stream_id."""
        stream_id = payload.get("stream_id")
        entries = []

        if self._path.exists():
            with open(self._path) as f:
                for line in f:
                    entry = json.loads(line)
                    if stream_id is None or entry.get("stream_id") == stream_id:
                        entries.append(entry)

        return {"result_status": "SUCCESS", "entries": entries}
