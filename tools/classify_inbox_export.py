#!/usr/bin/env python3
"""Classify mailbox/message exports for a job pipeline.

This tool is intentionally offline and provider-neutral. It reads a JSON or JSONL
export that you create elsewhere and emits a JSONL triage stream. It does not
connect to Gmail, LinkedIn, an ATS, or any other live service.

Expected input fields are flexible; common names are supported:
  id, thread_id, source, from, sender, subject, snippet, body, date, url
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


HIGH_SIGNAL = re.compile(
    r"\b(interview|offer|onboarding|background|screen|next step|schedule|rate|salary|compensation|"
    r"w2|c2c|1099|contract|direct hire|remote|client|submitted|application received)\b",
    re.I,
)
LOW_FIT = re.compile(
    r"\b(onsite|hybrid|relocation required|sponsored|newsletter|digest|promo|webinar|survey)\b",
    re.I,
)
NO_REPLY = re.compile(r"\b(no[- ]?reply|do not reply|unattended mailbox|automated email)\b", re.I)
ADMIN = re.compile(r"\b(payroll|tax|insurance|background check|onboarding|i-9|benefits|account)\b", re.I)


def load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if not stripped:
        return []
    if stripped[0] == "[":
        data = json.loads(text)
        return [x for x in data if isinstance(x, dict)]
    if stripped[0] == "{":
        data = json.loads(text)
        if isinstance(data, dict):
            for key in ("messages", "items", "records", "conversations"):
                if isinstance(data.get(key), list):
                    return [x for x in data[key] if isinstance(x, dict)]
            return [data]
    records = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            item = json.loads(line)
            if isinstance(item, dict):
                records.append(item)
    return records


def text_of(item: dict[str, Any]) -> str:
    fields: Iterable[str] = (
        "from",
        "sender",
        "subject",
        "preview",
        "snippet",
        "body",
        "text",
    )
    return "\n".join(str(item.get(field, "")) for field in fields)


def classify(item: dict[str, Any]) -> dict[str, Any]:
    text = text_of(item)
    if NO_REPLY.search(text):
        bucket = "no-reply-evidence"
        action = "record evidence; do not reply directly"
    elif ADMIN.search(text):
        bucket = "admin-or-onboarding"
        action = "route to priority admin/onboarding queue"
    elif LOW_FIT.search(text) and not HIGH_SIGNAL.search(text):
        bucket = "suppress"
        action = "suppress unless a human overrides"
    elif HIGH_SIGNAL.search(text):
        bucket = "actionable"
        action = "review and draft next state-changing response"
    else:
        bucket = "review"
        action = "manual review"
    return {
        "id": item.get("id") or item.get("message_id") or item.get("thread_id") or item.get("url"),
        "source": item.get("source") or item.get("mailbox") or item.get("channel"),
        "sender": item.get("from") or item.get("sender"),
        "subject": item.get("subject") or item.get("title"),
        "bucket": bucket,
        "recommended_action": action,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify a JSON/JSONL inbox export for job-pipeline triage.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = [classify(item) for item in load_records(args.input)]
    output = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    if args.output:
        args.output.write_text(output + ("\n" if output else ""), encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
