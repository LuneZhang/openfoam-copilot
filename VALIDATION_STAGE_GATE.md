# Validation Stage Gate

Date: 2026-03-17
Status: GO

## Purpose

Define the exit criteria for the current validation/calibration pass that follows first-pass scenario expansion.

This stage gate exists to prevent two failure modes:
1. stopping after only one scenario family looks good
2. reopening uncontrolled expansion work when the real need was only a narrow routing calibration

## Intended milestone for this pass

The current validation/calibration stage is considered successful if:
- compressible, multiphase, and reacting families have each been checked against representative case classes
- routing behavior is sensible at the scenario, playbook, and node-selection layers
- any fixes applied are shallow, justified, and validation-driven
- no family still shows an unresolved weak-pass, misroute, or incomplete result in the current matrix

## Current checkpoint

### Matrix coverage
- compressible A1-A3: yes
- multiphase B1-B3: yes
- reacting C1-C3: yes

### Validation outcome quality
- pass: yes, across all nine representative case classes
- weak-pass remaining: no
- misrouted remaining: no
- incomplete remaining: no

### Calibration discipline
- shallow routing/playbook fixes only: yes
- unnecessary new-node expansion avoided: yes
- official/community traceability discipline preserved: yes

## Key fixes that justified closure

1. residual-routing calibration
- residual-focused routing now carries the startup/structure-sensitive handoffs needed for compressible and reacting validation

2. reacting naming/routing cleanup
- playbook references now point to the canonical reacting template name
- the older reacting template remains only as a compatibility alias instead of a competing live branch

## Exit criteria

This validation/calibration pass can be considered closed when all of the following are true:

### Required
1. all three target scenario families pass their representative validation case classes
2. no remaining result is classified as weak-pass, misrouted, or incomplete in the active matrix
3. any fixes made are the shallowest reasonable fixes
4. the next step is defined as controlled deepening or future replay validation, not broad first-pass expansion

### Nice to have
- one explicit cross-family asymmetry note
- one explicit stage-gate document marking whether the repository can leave validation mode

## Decision

Current recommendation: **GO**.

The present validation matrix is complete for the current first-pass scope.
The observed asymmetries were narrow and have been calibrated without reopening expansion sprawl.
The repository can leave the validation/calibration stage for this scope.

## What should happen next

The preferred next step is one of these, but not all at once:
1. controlled second-pass deepening for the highest-value family
2. replay validation against real external failure logs
3. selective traceability strengthening only where future case evidence shows it is needed

## What should not happen next

- do not restart broad first-pass scenario expansion
- do not add new nodes without a case-driven miss
- do not let one family monopolize deeper specialization before a concrete need is shown
