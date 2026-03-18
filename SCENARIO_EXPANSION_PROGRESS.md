# Scenario Expansion Progress

Date: 2026-03-16
Status: first-pass closure complete; validation path initialized

## Purpose

Track the current scenario-expansion pass that follows the completed troubleshooting-foundation stage.

This file exists to answer:
- which scenario families now have a real first-pass closure?
- what is still missing before this scenario-expansion pass can be considered complete?
- what should happen next without reopening uncontrolled branch sprawl?

## Current objective

Extend the completed troubleshooting/routing foundation across the three higher-value scenario families that were intentionally deferred:
1. compressible thermo flow
2. multiphase interface flow
3. reacting / combustion flow

The target is not deep specialization yet.
The target is a **first-pass closed loop** for each family:
- scenario template
- scenario-to-node routing
- setup / case-review tightening
- at least one narrow troubleshooting node

## Status by scenario family

### 1) Compressible thermo flow
Status: **first-pass closed loop complete**

Delivered:
- scenario template refinement
- scenario routing refinement
- setup / case-review tightening
- narrow node: `compressible-steady-startup-too-brittle`

What this now enables:
- agents distinguish thermo/BC structure issues from pure numerics earlier
- agents treat brittle steady startup as a first-class branch rather than a vague hint

### 2) Multiphase interface flow
Status: **first-pass closed loop complete**

Delivered:
- scenario template refinement
- scenario routing refinement
- setup / case-review tightening
- narrow node: `multiphase-interface-initialization-mismatch`

What this now enables:
- agents treat interface topology and phase initialization as structural setup problems
- agents route multiphase serial/parallel interface issues more coherently

### 3) Reacting / combustion flow
Status: **first-pass closed loop complete**

Delivered:
- scenario template creation + refinement
- scenario routing refinement
- setup / case-review tightening
- narrow node: `reacting-startup-coupling-too-stiff`

What this now enables:
- agents distinguish reacting structure problems from generic stiffness complaints earlier
- agents can recommend staged/transient startup when the reacting branch is structurally plausible but too stiff for the current launch path

## Overall assessment

### Achieved
- all three deferred scenario families now have a real first-pass closed loop
- prompt-layer and troubleshooting entry behavior now generalize beyond the original foundation scenarios
- the repository no longer depends on only one or two scenario classes to demonstrate the routing workflow

### Not yet complete
- no case-based validation set has yet been run across all three new scenario families
- deeper scenario-specific sub-branches are intentionally deferred
- validation findings are only beginning to be converted into replay-tested fixes

## Recommended interpretation

Do not treat this scenario-expansion pass as “finished forever.”
Treat it as having completed the **first-pass closure milestone** for the three main deferred scenario families.

That is enough to justify moving from expansion to:
1. consistency audit
2. stage-gate decision
3. next validation or deepening step

## Next recommended move

Run the validation path using `VALIDATION_CASE_MATRIX.md` and `VALIDATION_WORKFLOW.md` instead of immediately adding more narrow nodes.

That path should verify:
- setup / review / troubleshooting prompts tell the same story in live case-style use
- each scenario family routes into sensible first branches
- future fixes are case-driven or validation-driven, not just more branch accumulation
