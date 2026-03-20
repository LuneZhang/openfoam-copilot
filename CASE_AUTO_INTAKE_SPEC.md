# Case Auto-Intake Specification

Date: 2026-03-19
Status: aligned-v1

## Purpose

Define the internal auto-intake contract for agents debugging an OpenFOAM-style case from a filesystem path.

This specification is **not** a user-facing form.
The user should not be asked to fill this out manually unless helper execution is unavailable.

The intended workflow is:
1. user gives a case path
2. agent inspects the case automatically
3. agent builds a structured intake summary internally
4. only then does the agent choose scenario / playbook / node routing

The canonical machine-readable contract for the helper lives at `runtime/catalog/auto-intake.json`.

## User-facing input contract

The minimum expected user input is:
- a case path

Optional helpful input:
- a log path
- a short failure description
- whether the failure happened in serial or parallel

The agent should treat all other intake fields as auto-collected whenever helper execution is available.

If helper execution is unavailable, the fallback stays aligned with `runtime/contract.json`:
- ask only for the minimum manual inputs above
- do not ask the user to hand-fill the full structured output
- do not fake deeper diagnosis from missing auto-collected fields

## Supported output contract

The helper returns a single JSON object with these required top-level fields:
- `case_path`
- `case_name`
- `is_case_root`
- `structure_inventory`
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

### A. Case identity
- absolute case path
- stable case root name derived from the resolved path basename
- whether the directory looks like an OpenFOAM-style case root

### B. Structural inventory
- `structure_inventory` must always include:
  - `has_zero_dir`
  - `has_constant_dir`
  - `has_system_dir`
  - `has_post_processing_dir`
  - `has_processor_dirs`
  - `processor_dir_count`
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
- which root-level `log*` or `*.log` files are present

### D. Scenario-family hints
The auto-intake layer should attempt a first heuristic classification into:
- compressible
- multiphase
- reacting
- incompressible-or-unknown fallback as `incompressible_or_unknown`

This classification can be heuristic, but the reasons should be recorded.

### E. Pressure convention hints
Attempt to detect:
- `p`
- `p_rgh`
- both
- neither

### F. Failure-signal extraction
If logs exist, attempt to extract signals such as:
- `floating_point_exception`
- `continuity_error`
- `courant_issue`
- `ami_or_interface`
- `processor_boundary_issue`
- `residual_blowup`
- `bounding_or_clipping`
- `fatal_io_or_dictionary`

These tags are limited log-pattern hints. They are not mesh diagnosis, hotspot detection, or proof of root cause.

## Required output shape

The auto-intake layer should produce the exact required fields listed in the canonical contract at `runtime/catalog/auto-intake.json`.

Field intent is split into two groups:
- authoritative observations: `case_path`, `case_name`, `is_case_root`, `structure_inventory`, `application`, `key_files`, `zero_fields`, `log_files`
- heuristic routing hints: `scenario_family_guess`, `scenario_family_reasons`, `pressure_variable_hint`, `parallel_hint`, `failure_signals`, `recommended_first_read_order`, `notes`

## Recommended first-read output

The intake summary should recommend which repository files to read next, for example:
1. `TROUBLESHOOTING_ENTRY.md`
2. `playbooks/debug-routing/scenario-to-node-routing-v1.md`
3. `PARALLEL_TRIAGE_DECISION_TREE.md` if parallel markers or processor-related signals are present
4. `playbooks/debug-routing/playbook-to-node-routing-v1.md`
5. the closest scenario template and only directly supported starter nodes

This keeps auto-intake tightly connected to the existing routing system.

## Hard rules

- do not ask the user to hand-fill this structure unless helper execution is unavailable
- do not treat missing optional files as fatal if the case root still looks valid
- do not jump from file inventory directly to numerics advice; intake must feed routing, not replace routing
- do not claim mesh-hotspot detection, advanced diagnosis, or deeper routing certainty that the helper does not actually produce
- if the case path is not a recognizable case root, say so clearly and stop before pretending diagnosis has started

## Current intent

This first-pass spec is meant to support:
- path-driven debugging
- replay validation from local failure cases
- future automation scripts that summarize cases before routing
