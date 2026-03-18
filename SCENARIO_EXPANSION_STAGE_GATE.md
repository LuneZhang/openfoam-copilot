# Scenario Expansion Stage Gate

Date: 2026-03-16
Status: GO

## Purpose

Define the exit criteria for the current scenario-expansion pass.

This stage gate prevents two failure modes:
1. declaring success too early while one scenario family still lags behind the others
2. endlessly adding more scenario-specific branches without deciding whether the pass has already met its intended milestone

## Intended milestone for this pass

The current pass is considered successful if:
- compressible, multiphase, and reacting scenario families all have a first-pass closed loop
- the prompt and routing layers can enter those families coherently
- each family has at least one narrower troubleshooting branch beyond generic symptom buckets

## Current checkpoint

### Scenario-family closure
- compressible: yes
- multiphase: yes
- reacting: yes

### Prompt / routing closure
- setup assistant reflects all three families: yes
- case review reflects all three families: yes
- troubleshooting assistant reflects all three families: yes
- scenario-to-node routing covers all three families: yes
- playbook-to-node routing exposes the key narrower branches: yes

### Narrow-branch coverage
- compressible narrow branch exists: yes
- multiphase narrow branch exists: yes
- reacting narrow branch exists: yes

## Exit criteria

This scenario-expansion pass can be considered closed when all of the following are true:

### Required
1. all three target scenario families have a first-pass closed loop
2. the main prompt surfaces remain aligned with the routing docs
3. no scenario family is still missing its first narrow troubleshooting branch
4. the next step is defined as validation/deepening, not more open-ended first-pass expansion

### Nice to have
- one reviewer-facing progress summary
- one explicit note describing what is intentionally deferred

## Current recommendation

Current recommendation: **GO**.

The light consistency audit summary has been written and the validation path has been initialized.
The main scenario-expansion objective is no longer blocked by missing first-pass closure.
The repository should not stay in first-pass expansion mode any longer.

## What should happen next

The current chosen next step is:
1. validation path — test the current routing against representative cases

Alternative paths remain available later:
2. deepening path — choose one scenario family and add second-pass specialized sub-branches
3. verification path — strengthen official/community traceability where the new families still feel thin

## What should not happen next

- do not keep adding first-pass scenario templates indefinitely
- do not deepen all three scenario families at once
- do not reopen broad troubleshooting sprawl without a case-driven reason
