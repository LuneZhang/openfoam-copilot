# Troubleshooting Entry

## Purpose

This is the hand-authored troubleshooting wrapper for agents using this repository.

Use it to answer three questions early:
1. which scenario family is this case closest to?
2. is the problem mainly structural, numerical, mesh-driven, or parallel-sensitive?
3. which node family should be loaded first instead of searching broadly?

## Runtime source of truth

Use `runtime/generated/troubleshooting-entry.md` for the canonical troubleshooting order.

Treat these runtime files as the factual spine behind that generated view:
- `runtime/contract.json`
- `runtime/surface.json`
- `runtime/catalog/scenarios.json`
- `runtime/catalog/playbooks.json`
- `runtime/catalog/nodes.json`

This file adds classifier guidance after the generated path is chosen. It should not become a second routing table.

## Runtime boundary

- Default to runtime-facing troubleshooting, routing, and knowledge files.
- Do not pull in `.sisyphus/`, stage-gate docs, progress logs, or validation reports unless the task is explicitly about repository status or validation history.

## How to use this file

1. Follow `runtime/generated/troubleshooting-entry.md` through helper/manual intake, scenario match, and routing playbooks.
2. Use the classifier guidance below to rank the first checks and choose the strongest node branch.
3. Keep `prompts/troubleshooting-assistant.md` aligned with the generated troubleshooting path rather than inventing a new order here.

## First classifier: serial vs parallel

### If serial is already clearly broken
Treat the case as a structural or setup-class problem first.

Prioritize:
- BC structure
- pressure convention / anchor semantics
- turbulence-field consistency
- mesh hotspots
- solver-family mismatch

### If serial is clean or much cleaner than parallel
Enter the parallel branch first:
- start with `parallel-only-failure`
- then use `PARALLEL_TRIAGE_DECISION_TREE.md`

## Second classifier: structural vs numerics-first

### Structural-first clues
Prefer structural nodes first when you see:
- patch/field mismatch
- wrong pressure variable or anchor behavior
- reverse flow at outlet/opening
- turbulence family / patch-role confusion
- thermo package inconsistency
- compressible cases being treated with incompressible setup intuition
- multiphase cases being treated like single-phase setups with extra fields bolted on
- reacting cases being treated like non-reacting flow with chemistry/heat-release details bolted on
- failure immediately at startup before meaningful residual evolution

Typical nodes:
- `patch-name-boundary-mismatch`
- `outlet-backflow-role-confusion`
- `p-vs-p_rgh-confusion`
- `buoyant-pressure-anchor-reference-mismatch`
- `turbulence-field-startup-mismatch`
- `turbulence-field-family-patch-role-mismatch`
- `thermo-chemistry-package-inconsistency`
- `wrong-solver-family-selection`

### Mesh-first clues
Prefer mesh nodes first when you see:
- `checkMesh` warnings line up with instability
- instability localizes near a small region, wall layer, outlet, plume, or interface
- the case survives only under excessively conservative numerics

Typical nodes:
- `mesh-quality-driven-instability`
- `critical-region-local-mesh-hotspot`
- `localized-divergence-hotspot-triage`

### Numerics-first clues
Prefer numerics/stability nodes first only after structural and mesh checks are not dominant.

Typical nodes:
- `steady-state-divergence-overaggressive-numerics`
- `courant-driven-transient-instability`
- `residual-plateau-fake-convergence`
- `continuity-error-growth`

## Third classifier: local hotspot vs global fragility

Ask early:
- does the case fail everywhere, or first in one small region?
- is the first failing region tied to a patch, interface, plume, wake, wall layer, or tiny geometric feature?

### If one region dominates early
Prefer hotspot routing first:
- `localized-divergence-hotspot-triage`
- then `critical-region-local-mesh-hotspot` or a narrower BC/interface node

### If the whole case is broadly unstable
Use wider numerics / continuity / solver-family routing.

## Fourth classifier: evidence tier

When the agent makes recommendations:
- official OpenFOAM docs are the primary truth layer
- community evidence is a bounded heuristic layer
- distilled rules are routing accelerators, not replacements for source-backed review

If official and community guidance conflict:
- prefer official guidance
- keep the community heuristic only as a lower-confidence branch clue

## Anti-patterns

Do not let the agent do these too early:
- jump straight to relaxation factors
- tune timestep before checking whether BC / mesh / solver family is structurally wrong
- search broadly before choosing scenario + playbook + node
- treat every parallel failure as decomposition-only
- treat every outlet-local failure as numerics-only
- trust average mesh quality over the first unstable region

## Recommended companion surfaces

- `runtime/generated/troubleshooting-entry.md`
- `CASE_AUTO_INTAKE_SPEC.md`
- `CASE_TRIAGE_PLAYBOOK.md`
- `PARALLEL_TRIAGE_DECISION_TREE.md`
- `prompts/troubleshooting-assistant.md`
