# Publishable Job-Pipeline Tools

This repository includes only reusable, offline, dry-run tooling for an agent-assisted job pipeline.

## Included

- `tools/classify_inbox_export.py`: classifies a JSON/JSONL mailbox or message export into actionable, admin/onboarding, no-reply evidence, suppress, or review buckets.
- `tools/classify_message_export.py`: classifies exported recruiter or messaging threads and reports which qualification gates are present or missing.
- `tools/update_pipeline_state.py`: upserts a JSONL system-of-record row for an opportunity.

## Not Included

- Credentials, OAuth tokens, API keys, browser profiles, or `.env` files.
- Live Gmail, LinkedIn, ATS, calendar, or browser-login automation.
- Resume files, mailbox exports, screenshots, or private candidate data.
- Auto-send or auto-apply behavior.

## Example

```powershell
python tools/classify_inbox_export.py examples/inbox-export.example.json
python tools/classify_message_export.py examples/inbox-export.example.json
python tools/update_pipeline_state.py .local/pipeline.jsonl --company ExampleCo --role "AI Engineer" --stage qualified --next-action "Ask for rate and interview timeline"
```

The `.local/` directory is ignored and is intended for private local state.
