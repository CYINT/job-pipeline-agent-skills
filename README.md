# Job Pipeline Agent Skills

Reusable OpenCode skills for operating an agent-assisted job-search and lead-touch follow-up pipeline.

These skills are deliberately process-only. They do not include credentials, browser profiles, private contact lists, mailbox exports, resumes, or proprietary candidate data.

## Skills

- `job-pipeline-operator`: designs and operates a bounded job-search pipeline from role discovery through offer acceptance.
- `lead-touch-follow-up`: classifies inbound leads and drafts safe, high-signal follow-up without over-messaging.

## Install

Copy the skill directories into an OpenCode skill path, for example:

```powershell
Copy-Item -Recurse .\.opencode\skills\* "$HOME\.config\opencode\skills"
```

Then restart OpenCode so the skills are loaded.

## Operating Limits

The skills are written to avoid common failure modes:

- No credential handling.
- No mass messaging.
- No automated application submission without human approval.
- No fabrication of experience, compensation, authorization, or availability.
- No duplicate submissions to the same company or role.
- No outreach without a concrete reason, evidence, and next action.
- Human approval is required before sending external messages or accepting representation terms.

## Suggested System Of Record

Use a simple table, spreadsheet, database, or Markdown-backed repo with these entities:

- `company`
- `role`
- `contact`
- `source`
- `application`
- `conversation`
- `touch`
- `decision`
- `artifact`

The important design choice is not the storage engine. It is preserving evidence, state, next action, and suppression rules in one place.

## License

MIT. See `LICENSE`.
