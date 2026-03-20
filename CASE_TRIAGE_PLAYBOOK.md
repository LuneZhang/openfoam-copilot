# Case Triage Playbook

Date: 2026-03-19
Status: aligned-v1

## Purpose

Define how an agent should move from an automatically collected case snapshot to the repository's scenario -> playbook -> node routing workflow.

This playbook assumes the agent already has a case path and has either run the auto-intake helper or fallen back to the minimum manual inputs from `runtime/contract.json`.

If helper execution is unavailable, ask only for:
- case path
- optional log path
- optional short failure description
- optional serial-vs-parallel hint

Do not fabricate the rest of the intake object.

## Workflow

### Step 1 — Verify that this is really a case root
Use `is_case_root` plus `structure_inventory`.

If `0/`, `constant/`, and `system/` are not all recognizable, stop and report that the supplied path is not yet a usable case root.

Do not fake deeper diagnosis from a non-case directory.

### Step 2 — Choose the scenario family
Use the auto-intake output to choose the closest family:
- compressible
- multiphase
- reacting
- `incompressible_or_unknown`

Then load the closest file under `scenario_templates/`.

Treat `scenario_family_guess` as a starting branch only. If the helper reports `incompressible_or_unknown`, stay broad and let the routing playbooks narrow the path.

### Step 3 — Choose the first classifier
Before loading nodes, ask:
1. does this look structural-first?
2. is it serial-clean but parallel-bad?
3. do the supported log signals point to a startup, continuity, Courant, or processor-boundary branch?
4. if not, does the broader troubleshooting entry still point to mesh or numerics checks after routing?

Use `TROUBLESHOOTING_ENTRY.md` as the top-level classifier.

Do not infer hotspot or advanced mesh diagnosis from auto-intake alone.

### Step 4 — Enter scenario routing
Read:
- `playbooks/debug-routing/scenario-to-node-routing-v1.md`

Use the selected scenario family plus the supported failure signals from auto-intake to narrow likely branches.

### Step 5 — Enter playbook routing
Read:
- `playbooks/debug-routing/playbook-to-node-routing-v1.md`

Choose the closest playbook for the symptom class:
- case setup
- divergence recovery
- residual diagnosis
- mesh-quality repair
- boundary-condition design

### Step 6 — Load the top troubleshooting nodes
Load only the top 1–3 nodes first.
Do not start with broad search if the routing already points clearly.

Treat `recommended_first_read_order` as a convenience queue, not a replacement for reading the routing files.

### Step 7 — Escalate only if needed
If the first branch does not fit the evidence:
- patch the branch choice
- do not immediately add new nodes
- keep the escalation shallow and justified

## Auto-intake to routing examples

### Example A — compressible case, `application` present, `thermophysicalProperties` present, startup blows up immediately
Likely route:
- compressible scenario template
- setup or divergence playbook
- `thermo-chemistry-package-inconsistency`
- `wrong-solver-family-selection`
- `compressible-steady-startup-too-brittle`

### Example B — multiphase case with `alpha.*` fields and `p_rgh`, interface behavior unstable from the first time step
Likely route:
- multiphase scenario template
- setup or divergence playbook
- `multiphase-interface-initialization-mismatch`
- `p-vs-p_rgh-confusion`

### Example C — reacting case with thermo/chemistry files present, violent startup or strong thermal-release symptoms
Likely route:
- reacting scenario template
- setup or divergence playbook
- `thermo-chemistry-package-inconsistency`
- `reacting-startup-coupling-too-stiff`

### Example D — serial-clean, parallel-bad with processor-local errors
Likely route:
- scenario family first
- then `PARALLEL_TRIAGE_DECISION_TREE.md`
- then parallel-specific nodes before generic numerics advice

## Hard rules

- auto-intake is a routing aid, not a replacement for scenario/playbook/node logic
- do not let raw file inventory flatten diagnosis into keyword matching only
- do not treat hotspot, mesh-local, or deeper root-cause claims as established unless later routing evidence supports them
- prefer the shallowest correction when a validation miss is found
- only ask the user for more information after auto-intake and routing both fail to produce a credible first branch

## What to ask the user only if needed

If automatic triage is still underdetermined, ask only for the smallest missing items, for example:
- which log file corresponds to the failure?
- did it fail in serial, parallel, or both?
- which run attempt is the most recent failing one?

Keep follow-up questions minimal and evidence-driven.
