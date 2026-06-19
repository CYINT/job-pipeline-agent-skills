#!/usr/bin/env python3
"""Classify recruiter/message-thread exports without logging into any service.

Input is JSON/JSONL containing conversation cards or thread records. The script
identifies likely action items and missing qualification gates. It never sends
messages and never reads credentials.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


GATES = {
    "client": re.compile(r"\b(client|hiring group|end client|team)\b", re.I),
    "compensation": re.compile(r"\b(rate|salary|compensation|bonus|\$\d+)\b", re.I),
    "work_model": re.compile(r"\b(w2|c2c|1099|contract|direct hire|fte|full[- ]time)\b", re.I),
    "location": re.compile(r"\b(remote|hybrid|onsite|travel|timezone|relocation)\b", re.I),
    "process": re.compile(r"\b(interview|timeline|submission|right to represent|rtr|exclusive)\b", re.I),
}
SUPPRESS = re.compile(r"\b(outlier|data annotation|survey|promo|newsletter|sponsored)\b", re.I)


def load(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if text.lstrip().startswith(("[", "{")) else None
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ("threadDetails", "conversations", "messages", "items"):
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
        return [data]
    rows = []
    for line in text.splitlines():
        if line.strip():
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
    return rows


def flatten_text(item: dict[str, Any]) -> str:
    parts = [str(item.get(k, "")) for k in ("name", "preview", "subject", "text", "body")]
    for msg in item.get("recentMessages", []) or item.get("messages", []) or []:
        if isinstance(msg, dict):
            parts.append(str(msg.get("sender", "")))
            parts.append(str(msg.get("text", "")))
    conv = item.get("conversation")
    if isinstance(conv, dict):
        parts.append(str(conv.get("name", "")))
        parts.append(str(conv.get("preview", "")))
    return "\n".join(parts)


def classify(item: dict[str, Any]) -> dict[str, Any]:
    text = flatten_text(item)
    present = sorted(name for name, pattern in GATES.items() if pattern.search(text))
    missing = sorted(set(GATES) - set(present))
    bucket = "suppress" if SUPPRESS.search(text) else ("ready-for-review" if len(missing) <= 2 else "needs-clarification")
    return {
        "contact": item.get("name") or (item.get("conversation") or {}).get("name"),
        "bucket": bucket,
        "present_gates": present,
        "missing_gates": missing,
        "send_status": "draft-only",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify exported job-pipeline message threads.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    output = "\n".join(json.dumps(classify(row), ensure_ascii=False, sort_keys=True) for row in load(args.input))
    if args.output:
        args.output.write_text(output + ("\n" if output else ""), encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
