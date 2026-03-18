# Playbook-to-Node Routing v1

## Purpose
Map operational playbooks to the troubleshooting nodes they should most often invoke.

## 1) first-pass-case-setup-checklist
Primary node handoff targets:
- `wrong-solver-family-selection`
- `patch-name-boundary-mismatch`
- `p-vs-p_rgh-confusion`
- `turbulence-field-startup-mismatch`
- `thermo-chemistry-package-inconsistency`
- `multiphase-interface-initialization-mismatch`
- `critical-region-local-mesh-hotspot`
- `steady-state-divergence-overaggressive-numerics`
- `compressible-steady-startup-too-brittle`
- `reacting-startup-coupling-too-stiff`

Reacting emphasis:
- if thermo package, chemistry model, or species-field structure is unclear, stay in setup-level diagnosis before numerics tuning

Use when:
- the case is new
- structure and solver-family fit are still uncertain
- debugging should begin at setup level, not numerics level

## 2) divergence-recovery-v1
Primary node handoff targets:
- `floating-point-exception-startup`
- `continuity-error-growth`
- `mesh-quality-driven-instability`
- `courant-driven-transient-instability`
- `steady-state-divergence-overaggressive-numerics`
- `compressible-steady-startup-too-brittle`
- `multiphase-interface-initialization-mismatch`
- `reacting-startup-coupling-too-stiff`
- `outlet-backflow-role-confusion`
- `parallel-only-failure`
- `processor-count-sensitive-parallel-failure`
- `processor-boundary-field-inconsistency`
- `decomposition-fragmented-hotspot-vs-interface-semantic-defect`

Use when:
- the case clearly blows up or destabilizes
- you need a highest-priority recovery order

## 3) residual-diagnosis-v1
Primary node handoff targets:
- `residual-plateau-fake-convergence`
- `continuity-error-growth`
- `steady-state-divergence-overaggressive-numerics`
- `courant-driven-transient-instability`
- `compressible-steady-startup-too-brittle`

Use when:
- residual behavior is the main observable symptom
- the run is not necessarily crashing, but convergence quality is suspect

## 4) boundary-condition-design-v1
Primary node handoff targets:
- `patch-name-boundary-mismatch`
- `outlet-backflow-role-confusion`
- `p-vs-p_rgh-confusion`
- `buoyant-pressure-anchor-reference-mismatch`
- `turbulence-field-startup-mismatch`
- `turbulence-field-family-patch-role-mismatch`
- `wrong-solver-family-selection`

Use when:
- BC structure is suspected to be wrong
- the case looks structurally inconsistent before numerics tuning

## 5) mesh-quality-repair-v1
Primary node handoff targets:
- `mesh-quality-driven-instability`
- `critical-region-local-mesh-hotspot`
- `floating-point-exception-startup`
- `continuity-error-growth`
- `courant-driven-transient-instability`

Use when:
- checkMesh warnings or local bad cells correlate with instability
- the mesh is likely the main driver rather than a secondary annoyance

## Routing rule for agents
1. choose the scenario template first
2. choose the most relevant playbook second
3. use the playbook-to-node map to select the top node set
4. only then expand to broad source search
