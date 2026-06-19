---
name: job-pipeline-operator
description: Use when operating or designing an agent-assisted job-search pipeline: role discovery, filtering, application tracking, inbox triage, recruiter screens, follow-up cadence, offer tracking, and conversion analysis.
---

# Job Pipeline Operator

Use this skill to run a bounded, evidence-driven job-search pipeline. The goal is not maximum activity. The goal is high-quality conversion from relevant opportunities to interviews, offers, and accepted work.

## Pipeline Stages

Track every opportunity through one stage:

1. `discovered`
2. `qualified`
3. `suppressed`
4. `applied`
5. `recruiter-screen`
6. `submitted-to-client`
7. `interviewing`
8. `offer-intent`
9. `offer-received`
10. `accepted`
11. `rejected-or-closed`

Do not let an item live in multiple active stages. Update the stage when new evidence arrives.

## Core Entities

Maintain a system of record with these fields where possible:

`company | role | contact | source | location posture | work model | compensation | stage | next action | next action date | evidence | suppression reason | last touch | thread id`

The storage medium can be a spreadsheet, database, CRM, or Markdown repo. The invariant is that every external action has source evidence and a next state.

## Daily Operating Loop

Run this loop before broad application volume:

1. Check priority inboxes and message surfaces.
2. Classify each inbound item as actionable, FYI, suppressed, or unrelated.
3. Handle high-signal recruiter/client movement before new applications.
4. Update the system of record after each application, reply, call, or interview.
5. Run application volume only after response handling is current.
6. End with a short status summary: new movement, sent touches, blocked items, waiting items, and tomorrow's first action.

## Qualification Gates

Before investing heavily, capture:

- Actual company or end client.
- Role title and core scope.
- Work model: W2, 1099, C2C, direct hire, subcontract.
- Compensation or rate range.
- Remote, hybrid, onsite, travel, and timezone constraints.
- Interview process and timeline.
- Submission, right-to-represent, exclusivity, and duplicate-submission terms.
- Work authorization and sponsorship assumptions.

If a gate is missing, ask for it. Do not assume it.

## Suppression Rules

Suppress or defer:

- Duplicate applications to the same role or company without an explicit reason.
- Roles that violate non-negotiable location, work authorization, or compensation constraints.
- Recruiter messages with no concrete role, client, rate, model, or process.
- Broad hiring-manager campaigns with no credible contact path.
- Automated assessments that displace higher-probability live opportunities.
- Threads where representation terms are unclear or risky.

## Application Volume Rule

Application volume is a secondary loop. It should not bury active conversations.

Use volume when:

- Inbound/recruiter response queue is current.
- Active interview/offer prep is current.
- Duplicate suppression has been applied.
- The role passes location, compensation, authorization, and fit filters.

## Decision Intelligence

Score opportunities with a small transparent rubric:

`fit | compensation | remote feasibility | decision-maker proximity | process clarity | duplicate risk | time cost | conversion evidence`

Prefer a simple 1-5 score per factor over opaque model output. Keep the rationale.

## Output Formats

For a daily review:

`Opportunity | Stage | Evidence | Next action | Owner | Due | Risk`

For a role decision:

`Apply / pass / ask-clarifying-question | Why | Missing gates | Evidence | Follow-up date`

For a funnel summary:

`Discovered | Qualified | Applied | Screens | Interviews | Offers | Accepted | Rejected | Active waiting`

## Safety Limits

- Do not fabricate experience, credentials, compensation, authorization, or availability.
- Do not send external messages without approval unless the operator explicitly delegated sending authority.
- Do not accept right-to-represent, exclusivity, background-check, or offer terms without human approval.
- Do not store secrets, private mailbox exports, or resumes in public repositories.
