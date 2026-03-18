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

This skill should stay thin. Do **not** copy the repository contents into the skill. Point the agent to the repository and follow its reading order.

## Core rule

Treat the external repository as the source of truth for:
- scenario templates
- playbooks
- troubleshooting nodes
- routing maps
- validation and stage-gate documents

Use this skill only to:
1. locate the repository
2. enter it through the correct files
3. enforce the repository's intended reading order

## Required preflight

Before relying on the repository, verify these files exist under `__OPENFOAM_COPILOT_PROJECT_PATH__`:
- `README.md`
- `AGENT_ENTRY.md`
- `TROUBLESHOOTING_ENTRY.md`
- `playbooks/debug-routing/scenario-to-node-routing-v1.md`
- `playbooks/debug-routing/playbook-to-node-routing-v1.md`

If these files are missing, stop and say the bridge skill is not configured correctly for this machine.

## Workflow for case setup tasks

When the user asks how to build, choose, or review an OpenFOAM case before running it:

1. Read `__OPENFOAM_COPILOT_PROJECT_PATH__/AGENT_ENTRY.md`
2. Follow the **For case setup tasks** reading order from that file
3. Identify the closest file under `__OPENFOAM_COPILOT_PROJECT_PATH__/scenario_templates/`
4. Use the setup and case-review prompts under:
   - `__OPENFOAM_COPILOT_PROJECT_PATH__/prompts/setup-assistant.md`
   - `__OPENFOAM_COPILOT_PROJECT_PATH__/prompts/case-review.md`
5. Prefer official knowledge files under `__OPENFOAM_COPILOT_PROJECT_PATH__/knowledge/official/`
6. Use community material only as secondary heuristic support

## Workflow for troubleshooting tasks

When the user asks about divergence, crashes, nonphysical results, unstable startup, or suspicious convergence:

**Step 0 — Auto-intake if case path is available**

If the user provides a case path (directory containing `0/`, `constant/`, `system/`):

1. Run the auto-intake script to collect case snapshot:
   ```bash
   python3 __OPENFOAM_COPILOT_PROJECT_PATH__/scripts/case_auto_intake.py <CASE_PATH> --format json
   ```
2. Use the output to understand:
   - scenario family hint
   - parallel status
   - key files present
   - failure signals from logs
   - recommended first read order

3. If the script is not available or fails, manually collect information per `CASE_AUTO_INTAKE_SPEC.md`

**Step 1 — Enter repository routing**

1. Read `__OPENFOAM_COPILOT_PROJECT_PATH__/TROUBLESHOOTING_ENTRY.md`
2. Identify the closest file under `__OPENFOAM_COPILOT_PROJECT_PATH__/scenario_templates/`
3. Read `__OPENFOAM_COPILOT_PROJECT_PATH__/playbooks/debug-routing/scenario-to-node-routing-v1.md`
4. If the case is serial-clean but parallel-bad, also read:
   - `__OPENFOAM_COPILOT_PROJECT_PATH__/PARALLEL_TRIAGE_DECISION_TREE.md`
5. Read `__OPENFOAM_COPILOT_PROJECT_PATH__/playbooks/debug-routing/playbook-to-node-routing-v1.md`
6. Load the top matching troubleshooting nodes from:
   - `__OPENFOAM_COPILOT_PROJECT_PATH__/ontology/troubleshooting-graph/nodes/`
7. Use official evidence first, then bounded community heuristics
8. Return an **ordered diagnosis path**, not a flat suggestion list

## Workflow for project-state / validation questions

When the user asks whether the repository is ready, validated, or what stage it is in, read these files first:
- `__OPENFOAM_COPILOT_PROJECT_PATH__/PHASE1_STAGE_GATE.md`
- `__OPENFOAM_COPILOT_PROJECT_PATH__/SCENARIO_EXPANSION_PROGRESS.md`
- `__OPENFOAM_COPILOT_PROJECT_PATH__/SCENARIO_EXPANSION_STAGE_GATE.md`
- `__OPENFOAM_COPILOT_PROJECT_PATH__/VALIDATION_RESULTS.md`
- `__OPENFOAM_COPILOT_PROJECT_PATH__/VALIDATION_STAGE_GATE.md`

Use those files to answer stage/progress/readiness questions instead of guessing from scattered repository contents.

## Hard rules

- Do not duplicate repository knowledge into the skill unless a very small bridge note is absolutely necessary.
- Do not skip the repository's reading order.
- Do not jump straight to numerics tuning when the repository routes the case into a structure-first branch.
- Prefer official OpenFOAM guidance over community heuristics when the repository marks a conflict.
- If the repository and the skill ever disagree, follow the repository and update the skill later.
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
