#!/usr/bin/env python3
"""Append or update a JSONL job-pipeline state file.

This is a small local system-of-record helper. It stores only the fields you
provide on the command line and is safe for public distribution because it has
no built-in identity, credentials, URLs, or service integrations.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGES = {
    "discovered",
    "qualified",
    "suppressed",
    "applied",
    "recruiter-screen",
    "submitted-to-client",
    "interviewing",
    "offer-intent",
    "offer-received",
    "accepted",
    "rejected-or-closed",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
    return rows


def key_of(row: dict[str, Any]) -> str:
    return "|".join(str(row.get(k, "")).strip().lower() for k in ("company", "role", "source_id"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Upsert a job-pipeline state row into a JSONL file.")
    parser.add_argument("state", type=Path)
    parser.add_argument("--company", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--stage", required=True, choices=sorted(STAGES))
    parser.add_argument("--source-id", default="")
    parser.add_argument("--contact", default="")
    parser.add_argument("--next-action", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--suppression-reason", default="")
    args = parser.parse_args()

    row = {
        "company": args.company,
        "role": args.role,
        "source_id": args.source_id,
        "contact": args.contact,
        "stage": args.stage,
        "next_action": args.next_action,
        "evidence": args.evidence,
        "suppression_reason": args.suppression_reason,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    rows = read_jsonl(args.state)
    target_key = key_of(row)
    replaced = False
    for idx, existing in enumerate(rows):
        if key_of(existing) == target_key:
            rows[idx] = {**existing, **row}
            replaced = True
            break
    if not replaced:
        rows.append(row)
    args.state.parent.mkdir(parents=True, exist_ok=True)
    args.state.write_text("\n".join(json.dumps(item, sort_keys=True) for item in rows) + "\n", encoding="utf-8")
    print(json.dumps({"updated": True, "inserted": not replaced, "count": len(rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
