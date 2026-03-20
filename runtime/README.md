# Runtime Contract

This directory defines the initial portable runtime contract for external coding agents that consume this repository from local files.

## Default consumption model

Read `runtime/contract.json` first. The supported model is local-files-first:

1. Open the repository-local entry surfaces.
2. Follow their ordered reading and routing into authored Markdown.
3. Treat executable helpers as optional convenience only.

The contract makes no network, package-manager, or service-process assumptions.

## Runtime entrypoints

Use these files as the default runtime entry surface:

- `README.md`
- `AGENT_ENTRY.md`
- `TROUBLESHOOTING_ENTRY.md`
- `CASE_AUTO_INTAKE_SPEC.md`
- `CASE_TRIAGE_PLAYBOOK.md`
- `references/retrieval-order.md`
- `skills/openfoam-copilot/SKILL.md`

Those entrypoints route into the authored runtime content under `playbooks/`, `scenario_templates/`, `ontology/`, `knowledge/`, and `prompts/`.

## Optional helper use

Use `scripts/case_auto_intake.py` only when a local case path is available and local Python execution is available.

If the helper cannot run, fall back to the manual intake described in `CASE_AUTO_INTAKE_SPEC.md`, then continue with `CASE_TRIAGE_PLAYBOOK.md` and `TROUBLESHOOTING_ENTRY.md`.

## Boundary

Human-authored Markdown remains the primary runtime knowledge surface. Project-state, planning, progress, and validation-status documents are outside the default runtime dependency surface and should only be consulted for maintenance or repository-status questions.
