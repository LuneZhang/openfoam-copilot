# OpenFOAM Tutorial for Agent

This project is a structured OpenFOAM knowledge base designed for agent reuse.

Current status: the troubleshooting-foundation pass and the first-pass scenario-expansion pass have both been closed out; the project has now entered validation-path planning for representative case-based routing checks.

See:
- `MASTER_PLAN.md`
- `DETAILED_DESIGN_V2.md`
- `TROUBLESHOOTING_ENTRY.md`
- `PARALLEL_TRIAGE_DECISION_TREE.md`
- `PHASE1_STAGE_GATE.md`
- `NEXT_STAGE_STARTUP_CHECKLIST.md`
- `SCENARIO_EXPANSION_PROGRESS.md`
- `SCENARIO_EXPANSION_STAGE_GATE.md`
- `VALIDATION_CASE_MATRIX.md`
- `VALIDATION_WORKFLOW.md`
- `CASE_AUTO_INTAKE_SPEC.md`
- `CASE_TRIAGE_PLAYBOOK.md`

Primary objective:
- help agents set up OpenFOAM cases correctly
- help agents diagnose divergence, crashes, and nonphysical results
- support path-driven case auto-intake so agents can inspect a case directory directly
- separate official guidance from community heuristics
- provide reusable playbooks instead of loose notes

## Installation for Coding Agents

### Install the bridge skill

1. Download `skills/openfoam-copilot.skill`
2. Extract to your agent's skills directory
3. Replace `__OPENFOAM_COPILOT_PROJECT_PATH__` with the actual path to this repository

### Usage

After installing the skill, your coding agent will:
1. Automatically run `scripts/case_auto_intake.py` when given a case path
2. Follow the troubleshooting routing defined in this repository
3. Load appropriate scenario templates and troubleshooting nodes

