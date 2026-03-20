# AGENT_ENTRY.md

This is the hand-authored wrapper for agents entering the runtime surface for setup and case-review work.

## Runtime source of truth

Use `runtime/generated/agent-entry.md` as the current generated runtime view for entry behavior.

Treat these runtime files as the canonical spine behind that generated view:
- `runtime/contract.json`
- `runtime/surface.json`
- `runtime/catalog/*.json`

This file stays task-facing. It should not become a second routing map.

## Runtime boundary

- Default to runtime entry surfaces, generated views, and authored runtime content under `playbooks/`, `scenario_templates/`, `ontology/`, `knowledge/`, and `prompts/`.
- Do not treat `.sisyphus/`, stage-gate docs, progress logs, or validation reports as default runtime dependencies.
- Use project-state material only when the user is explicitly asking about repository status, migration, or validation history.

## How to use this surface

### Setup tasks
1. Read `runtime/generated/agent-entry.md`.
2. Follow its case-setup lane and `runtime/generated/retrieval-order.md`.
3. Match the closest scenario template.
4. Start from `playbooks/case-setup/first-pass-case-setup-checklist.md`.
5. Use `prompts/setup-assistant.md` to shape the answer.

### Case-review tasks
1. Read `runtime/generated/agent-entry.md`.
2. Follow its case-review lane and `runtime/generated/retrieval-order.md`.
3. Match the closest scenario template before widening into playbooks or nodes.
4. Use `prompts/case-review.md` to keep the review structural and risk-aware.

### Troubleshooting handoff

If the task is already about failure diagnosis, switch to `runtime/generated/troubleshooting-entry.md` and then continue with `TROUBLESHOOTING_ENTRY.md` for classifier-specific guidance.

## Hard rules

- Keep scenario -> playbook -> node order before broad source search.
- Prefer official OpenFOAM guidance over community heuristics when they conflict.
- Preserve source traceability for important claims.
- Explain solver, model, and BC assumptions when setup choices are not unique.
- Do not let project-state documents become default runtime dependencies.
