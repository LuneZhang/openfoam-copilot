# OpenFOAM Copilot

This repository is a local-files-first OpenFOAM knowledge base for coding agents. It helps agents set up cases, review case structure, and troubleshoot divergence, crashes, or nonphysical results while keeping official guidance separate from bounded community heuristics.

## Supported Integration Paths

### 1. Full repository locally (default)

Use the full repository when the agent is working on the same machine as this checkout and can read the repo directly.

Start with:
- `README.md`
- `runtime/contract.json`
- `runtime/generated/skill-bridge.md`
- `runtime/generated/agent-entry.md`
- `runtime/generated/troubleshooting-entry.md`

This is the default integration path because it keeps the full authored runtime surface available locally.

### 2. Minimal runtime bundle export

Use the bundle export when a consumer only needs the portable runtime surface instead of the full repository.

Export it from the repository root with:

```bash
python3 scripts/export_runtime_bundle.py --out dist/openfoam-copilot-runtime
```

The exported bundle keeps repository-relative paths intact and includes the runtime contract, runtime surface definition, catalogs, generated runtime views, required authored runtime assets, source-traceability support, the optional auto-intake helper, and the skill bridge template. It excludes project-state material by default.

After export, point the consumer at `dist/openfoam-copilot-runtime/` and use that directory as the local runtime root.

## Skill Bridge Template

Use `skills/openfoam-copilot/SKILL.md` as the thin bridge template for either the full repository or an exported runtime bundle. Replace `__OPENFOAM_COPILOT_PROJECT_PATH__` with the real local path to the chosen root.

The primary readable bridge and routing surfaces are:
- `runtime/generated/skill-bridge.md`
- `runtime/generated/agent-entry.md`
- `runtime/generated/troubleshooting-entry.md`
- `runtime/generated/retrieval-order.md`

## Optional Helper

If local Python is available and a case path is available, the consumer may run:

```bash
python3 scripts/case_auto_intake.py <CASE_PATH> --format json
```

If the helper cannot run, fall back to the manual intake described by `CASE_AUTO_INTAKE_SPEC.md` and continue through `CASE_TRIAGE_PLAYBOOK.md` and `TROUBLESHOOTING_ENTRY.md`.
