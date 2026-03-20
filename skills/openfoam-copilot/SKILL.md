---
name: openfoam-copilot
description: Bridge skill that lets another agent consume an external `openfoam-copilot` repository by local path. Use when an agent needs OpenFOAM case setup, case review, divergence/crash troubleshooting, routing-aware diagnosis, or parallel-triage guidance from a separately maintained project repository rather than from knowledge embedded directly in the skill.
---

# OpenFOAM Copilot Bridge Skill

## Overview

Use this skill as a thin adapter in front of an existing `openfoam-copilot` repository.

Before using this skill, replace every occurrence of:

`__OPENFOAM_COPILOT_PROJECT_PATH__`

with the real absolute path to the project root on the current machine.

This skill should stay thin. Do not copy repository contents into the skill. Point the agent to the repository and follow its runtime surface.

## Runtime source of truth

Treat these files under `__OPENFOAM_COPILOT_PROJECT_PATH__` as the runtime spine:
- `runtime/contract.json`
- `runtime/surface.json`
- `runtime/generated/skill-bridge.md`
- `runtime/generated/agent-entry.md`
- `runtime/generated/troubleshooting-entry.md`
- `runtime/generated/retrieval-order.md`

Use the generated views for readable routing. If a generated view and canonical runtime metadata ever disagree, prefer the canonical runtime metadata.

## Core rule

Treat the external repository as the source of truth for scenario templates, playbooks, troubleshooting nodes, routing metadata, and source-traceability support.

Do not treat validation, stage-gate, progress, or `.sisyphus/` documents as default runtime truth.

Use this skill only to:
1. locate the repository
2. verify the runtime surface exists
3. route the agent into the repository's generated views and authored content

## Required preflight

Before relying on the repository, verify these files exist under `__OPENFOAM_COPILOT_PROJECT_PATH__`:
- `README.md`
- `AGENT_ENTRY.md`
- `TROUBLESHOOTING_ENTRY.md`
- `CASE_AUTO_INTAKE_SPEC.md`
- `CASE_TRIAGE_PLAYBOOK.md`
- `references/retrieval-order.md`
- `runtime/contract.json`
- `runtime/surface.json`
- `runtime/generated/skill-bridge.md`
- `runtime/generated/agent-entry.md`
- `runtime/generated/troubleshooting-entry.md`
- `runtime/generated/retrieval-order.md`

If these files are missing, stop and say the bridge skill is not configured correctly for this machine.

## Task handoff

- For case setup or case review:
  - open `__OPENFOAM_COPILOT_PROJECT_PATH__/runtime/generated/skill-bridge.md`
  - open `__OPENFOAM_COPILOT_PROJECT_PATH__/runtime/generated/agent-entry.md`
  - follow the repository's authored entry and runtime-generated entry surfaces from there

- For troubleshooting:
  - if a local case path is available and Python is available, the optional helper may be run first:
    ```bash
    python3 __OPENFOAM_COPILOT_PROJECT_PATH__/scripts/case_auto_intake.py <CASE_PATH> --format json
    ```
  - then open `__OPENFOAM_COPILOT_PROJECT_PATH__/runtime/generated/troubleshooting-entry.md`
  - use `__OPENFOAM_COPILOT_PROJECT_PATH__/TROUBLESHOOTING_ENTRY.md` only as the authored classifier companion after the generated entry surface is chosen

- For repository-status questions:
  - project-state documents may be consulted only when the user is explicitly asking about repository status, migration progress, or validation history

Do not use project-state documents to drive case setup, troubleshooting, case review, or runtime routing.

## Hard rules

- Do not duplicate repository knowledge into the skill unless a very small bridge note is absolutely necessary.
- Do not skip the runtime-generated entry and routing views.
- Keep the bridge limited to repository access, runtime verification, document handoff, and boundary enforcement.
- Let the model do the actual judgment; the bridge is navigation, not diagnosis.
- If the runtime-generated views and this skill ever disagree, follow the generated views and canonical runtime metadata.
- Keep the skill path placeholder easy to replace; do not hardcode a machine-specific path in the template version.

## Recommended placeholder to replace

Use a single absolute-path replacement target everywhere:

`__OPENFOAM_COPILOT_PROJECT_PATH__`

Example after user editing:
- `/home/yourname/projects/openfoam-copilot`
- `/Users/yourname/openfoam/openfoam-copilot`
- `D:/workspace/openfoam-copilot`

## Minimal installation/edit step for the user

After copying this template onto another machine:
1. replace `__OPENFOAM_COPILOT_PROJECT_PATH__` with the real local path
2. save the file
3. then let the target agent use the skill normally

That is the only machine-specific customization this template should require.
