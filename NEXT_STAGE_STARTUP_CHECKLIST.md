# Next Stage Startup Checklist

## Suggested next stage

Phase 3-style scenario expansion and validation, using the stronger troubleshooting/routing foundation already built.

## Why this should be next

The current repository is no longer missing its core debugging skeleton.
The highest-value next move is to test and extend that skeleton across more scenario families instead of continuing open-ended branch expansion.

## Priority order

### 1. Compressible thermo flow
Reason:
- high practical value
- stresses pressure, thermo, and transient startup routing
- good test of whether the current troubleshooting entry generalizes beyond the existing branches

### 2. Multiphase interface flow
Reason:
- strong interaction with the new parallel/interface routing
- good stress test for pressure convention and interface-sensitive failure classification

### 3. Reacting / combustion flow
Reason:
- highest complexity
- best deferred until the compressible + multiphase patterns are cleaner

## Start conditions

Begin the next stage only if:
1. the current stage gate says GO
2. no major contradictions remain between prompt layer and routing docs
3. the next stage is scoped as scenario expansion + validation, not another uncontrolled troubleshooting sweep

Status on 2026-03-16:
- condition 1: satisfied
- condition 2: satisfied in the final closeout audit
- condition 3: satisfied by the current checklist scope

## First tasks for the next stage

1. add / refine the missing scenario templates:
   - compressible
   - multiphase
   - reacting / combustion
2. validate that each new scenario maps cleanly into the existing troubleshooting entry
3. patch only the routing gaps that block those scenario families
4. avoid broad new source collection unless a scenario validation step proves a real gap

Current progress note:
- compressible thermo flow has completed the first routing pass, setup/case-review tightening, and a first narrow troubleshooting-node pass
- multiphase interface flow has completed the first routing pass, setup/case-review tightening, and a first narrow troubleshooting-node pass
- reacting / combustion flow has completed the first routing pass, setup/case-review tightening, and a first narrow troubleshooting-node pass
- use `SCENARIO_EXPANSION_PROGRESS.md` and `SCENARIO_EXPANSION_STAGE_GATE.md` as the current closeout lens for this pass

## Anti-patterns for the next stage

- do not reopen wide troubleshooting-node expansion without a scenario-driven reason
- do not add many community sources before the scenario family actually needs them
- do not let prompt/routing docs drift behind scenario expansion

## Success standard for the next stage

At the end of the next stage, an agent should be able to:
- identify the closest scenario family faster
- apply the current troubleshooting framework to more realistic case classes
- reuse the same debugging order across compressible, multiphase, and reacting branches without falling back to broad search first

Closeout note:
- the first-pass scenario-expansion milestone is now complete; use `VALIDATION_CASE_MATRIX.md` and `VALIDATION_WORKFLOW.md` as the active next-step documents
