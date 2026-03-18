# Case Auto-Intake Specification

Date: 2026-03-17
Status: first-pass

## Purpose

Define the internal auto-intake contract for agents debugging an OpenFOAM-style case from a filesystem path.

This specification is **not** a user-facing form.
The user should not be asked to fill this out manually unless automatic collection fails.

The intended workflow is:
1. user gives a case path
2. agent inspects the case automatically
3. agent builds a structured intake summary internally
4. only then does the agent choose scenario / playbook / node routing

## User-facing input contract

The minimum expected user input is:
- a case path

Optional helpful input:
- a log path
- a short failure description
- whether the failure happened in serial or parallel

The agent should treat all other intake fields as auto-collected whenever possible.

## Required auto-collected fields

### A. Case identity
- absolute case path
- case root name
- whether the directory looks like an OpenFOAM-style case root
- whether `0/`, `constant/`, and `system/` exist

### B. Structural inventory
- top-level presence of:
  - `0/`
  - `constant/`
  - `system/`
  - `processor*`
  - `postProcessing/`
- key dictionary presence:
  - `system/controlDict`
  - `system/fvSchemes`
  - `system/fvSolution`
  - `system/decomposeParDict` if present
  - `constant/thermophysicalProperties` if present
  - `constant/turbulenceProperties` if present
  - `constant/transportProperties` if present
  - chemistry / multiphase dictionaries if present
- fields present under `0/`

### C. Execution hints
- `application` from `controlDict` if available
- whether the case appears serial-only, parallel-capable, or already decomposed
- whether recent log files are present

### D. Scenario-family hints
The auto-intake layer should attempt a first heuristic classification into:
- incompressible
- compressible
- multiphase
- reacting
- unknown

This classification can be heuristic, but the reasons should be recorded.

### E. Pressure convention hints
Attempt to detect:
- `p`
- `p_rgh`
- both
- neither

### F. Failure-signal extraction
If logs exist, attempt to extract signals such as:
- floating point exception
- continuity growth
- Courant number trouble
- AMI / coupled-patch / processor-boundary trouble
- residual blow-up
- bounding / clipping messages
- fatal I/O or dictionary mismatch

### G. Mesh / hotspot hints
Attempt to identify whether evidence suggests:
- global mesh warnings
- local hotspot suspicion
- interface-region fragility
- reacting hotspot fragility
- no clear mesh hint yet

## Required output shape

The auto-intake layer should produce a compact structured summary containing at least:
- `case_path`
- `is_case_root`
- `application`
- `scenario_family_guess`
- `scenario_family_reasons`
- `pressure_variable_hint`
- `parallel_hint`
- `key_files`
- `zero_fields`
- `log_files`
- `failure_signals`
- `recommended_first_read_order`
- `notes`

## Recommended first-read output

The intake summary should recommend which repository files to read next, for example:
1. closest scenario template
2. `playbooks/debug-routing/scenario-to-node-routing-v1.md`
3. `PARALLEL_TRIAGE_DECISION_TREE.md` if appropriate
4. the most likely top 1–3 troubleshooting nodes

This keeps auto-intake tightly connected to the existing routing system.

## Hard rules

- do not ask the user to hand-fill this structure unless automatic intake fails badly
- do not treat missing optional files as fatal if the case root still looks valid
- do not jump from file inventory directly to numerics advice; intake must feed routing, not replace routing
- if the case path is not a recognizable case root, say so clearly and stop before pretending diagnosis has started

## Current intent

This first-pass spec is meant to support:
- path-driven debugging
- replay validation from local failure cases
- future automation scripts that summarize cases before routing
