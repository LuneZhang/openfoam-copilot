# Validation Case Matrix

Date: 2026-03-19
Status: active; combustion family D-block added

## Purpose

Provide a compact validation matrix for checking whether the current routing system behaves sensibly across the newly expanded scenario families.

This is not yet a run-log.
It is the planned set of representative case classes the repository should be validated against next.

## Validation dimensions

For each representative case, validate:
1. closest scenario family selection
2. first-pass playbook choice
3. top 1–3 troubleshooting nodes
4. whether the first branch choice matches the observed symptom class
5. whether the recommendation order avoids obvious anti-patterns

## Case matrix

### A. Compressible thermo flow

#### A1. Structurally wrong thermo/solver pairing
Expected first branches:
- `wrong-solver-family-selection`
- `thermo-chemistry-package-inconsistency`

What should be true:
- agent should not start from generic numerics tuning
- agent should identify setup-class structural mismatch first

#### A2. Structurally plausible but brittle steady startup
Expected first branches:
- `compressible-steady-startup-too-brittle`
- `critical-region-local-mesh-hotspot` if a local region is dominant

What should be true:
- agent should suggest staged/transient startup before thrashing with generic steady numerics

#### A3. High-gradient local hotspot hidden by globally passable mesh
Expected first branches:
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

What should be true:
- agent should not over-trust average mesh quality

### B. Multiphase interface flow

#### B1. Wrong interface topology / phase initialization
Expected first branches:
- `multiphase-interface-initialization-mismatch`
- `p-vs-p_rgh-confusion` when pressure framing is also implicated

What should be true:
- agent should not treat the case as only timestep-limited
- agent should inspect initial phase topology explicitly

#### B2. Interface-region local mesh fragility
Expected first branches:
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

What should be true:
- agent should identify the interface-sensitive weak region before broad numerics retuning

#### B3. Serial-clean, parallel-bad interface failure
Expected first branches:
- `parallel-only-failure`
- `processor-boundary-field-inconsistency`
- `decomposition-fragmented-hotspot-vs-interface-semantic-defect`

What should be true:
- agent should route through the parallel tree, not skip to generic CFL advice

### C. Reacting / combustion flow

#### C1. Wrong reacting solver/thermo/chemistry structure
Expected first branches:
- `wrong-solver-family-selection`
- `thermo-chemistry-package-inconsistency`

What should be true:
- agent should flag reacting structure mismatch before speaking about chemistry stiffness

#### C2. Structurally plausible but startup coupling too stiff
Expected first branches:
- `reacting-startup-coupling-too-stiff`
- `critical-region-local-mesh-hotspot` if a hotspot dominates

What should be true:
- agent should propose staged/transient startup before generic numerics churn

#### C3. Hotspot-driven reacting instability
Expected first branches:
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

What should be true:
- agent should distinguish local hotspot behavior from whole-case reacting impossibility

### D. Narrow combustion family expansion

#### D1. Premixed combustion baseline with wrong progress-variable or ignition startup structure
Expected scenario branch:
- `premixed-combustion-baseline`
Expected playbook branch:
- `first-pass-case-setup-checklist`
Expected first branches:
- `premixed-ignition-or-flame-speed-model-mismatch`
- `reacting-startup-coupling-too-stiff`

What should be true:
- agent should check premixed progress-variable and ignition structure before falling back to generic reacting startup advice

#### D2. Nonpremixed diffusion flame with mismatched fuel and oxidizer stream states
Expected scenario branch:
- `nonpremixed-diffusion-flame`
Expected playbook branch:
- `boundary-condition-design-v1`
Expected first branches:
- `nonpremixed-mixture-fraction-or-stoichiometric-inlet-mismatch`
- `outlet-backflow-role-confusion`

What should be true:
- agent should inspect separated-stream species and reverse-flow state treatment before generic chemistry-stiffness tuning

#### D3. Buoyant fire compartment with opening and reference-state mismatch
Expected scenario branch:
- `buoyant-fire-compartment`
Expected playbook branch:
- `boundary-condition-design-v1`
Expected first branches:
- `firefoam-ventilation-radiation-or-hrr-coupling-mismatch`
- `buoyant-pressure-anchor-reference-mismatch`

What should be true:
- agent should treat ventilation openings, ambient return state, and modified-pressure framing as the first structural branch

#### D4. Partially premixed recirculating combustor with unstable return-state framing
Expected scenario branch:
- `partially-premixed-recirculating-combustor`
Expected playbook branch:
- `boundary-condition-design-v1`
Expected first branches:
- `recirculating-combustor-flame-holding-or-backflow-mismatch`
- `outlet-backflow-role-confusion`

What should be true:
- agent should review the recirculating mixture state and pilot/backflow structure before generic reacting startup damping

#### D5. Spray combustion that destabilizes at injection onset
Expected scenario branch:
- `spray-combustion`
Expected playbook branch:
- `divergence-recovery-v1`
Expected first branches:
- `spray-injection-evaporation-coupling-startup-fragility`
- `reacting-startup-coupling-too-stiff`

What should be true:
- agent should inspect parcel and injector structure before treating the case as only a generic reacting stiffness problem

## Minimum acceptance standard

The current routing system passes this matrix if, for each case class:
1. the scenario family is classified correctly
2. at least one of the top two selected nodes matches the intended first branch
3. the proposed first checks follow the branch logic already encoded in prompts and playbooks
4. the recommendation order avoids obvious anti-patterns (e.g. immediate relaxation-factor thrash)

## Recommended next use

Use this matrix as the basis for:
- synthetic case reviews
- replaying known failure cases
- future automated evaluation prompts or human audit sessions
