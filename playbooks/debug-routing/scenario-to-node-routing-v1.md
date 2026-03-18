# Scenario-to-Node Routing v1

## Purpose
Map common OpenFOAM scenario families to the troubleshooting nodes most likely to matter first.

This is not a proof engine. It is a routing shortcut for faster first-pass diagnosis.

## 1) Incompressible laminar internal flow
Primary nodes:
- `patch-name-boundary-mismatch`
- `residual-plateau-fake-convergence`
- `continuity-error-growth`
- `mesh-quality-driven-instability`
- `wrong-solver-family-selection`

Typical rationale:
- many failures here are structural or BC-driven rather than model-complexity driven
- fake convergence is especially relevant when steady assumptions are used too casually

## 2) Incompressible RANS external aerodynamics
Primary nodes:
- `turbulence-field-startup-mismatch`
- `turbulence-field-family-patch-role-mismatch`
- `steady-state-divergence-overaggressive-numerics`
- `mesh-quality-driven-instability`
- `critical-region-local-mesh-hotspot`
- `parallel-only-failure`
- `processor-count-sensitive-parallel-failure`
- `processor-boundary-field-inconsistency`
- `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- `patch-name-boundary-mismatch`
- `residual-plateau-fake-convergence`
- `wrong-solver-family-selection`

Typical rationale:
- turbulent external-flow startups are sensitive to turbulence field consistency, turbulence family / wall-patch semantics, local mesh hotspots, parallel decomposition sensitivity, external-domain BC logic, and numerics aggressiveness

## 3) Buoyant natural convection / room-scale thermal flow
Primary nodes:
- `p-vs-p_rgh-confusion`
- `buoyant-pressure-anchor-reference-mismatch`
- `thermo-chemistry-package-inconsistency`
- `continuity-error-growth`
- `courant-driven-transient-instability`
- `mesh-quality-driven-instability`
- `critical-region-local-mesh-hotspot`

Typical rationale:
- buoyancy cases often fail because pressure convention, hydrostatic anchor semantics, thermo framing, transient startup control, and local plume / near-wall mesh weakness are structurally wrong or numerically fragile

## 4) Compressible thermo flow
Primary nodes:
- `thermo-chemistry-package-inconsistency`
- `wrong-solver-family-selection`
- `patch-name-boundary-mismatch`
- `mesh-quality-driven-instability`
- `critical-region-local-mesh-hotspot`
- `courant-driven-transient-instability`
- `steady-state-divergence-overaggressive-numerics`
- `compressible-steady-startup-too-brittle`

Typical rationale:
- compressible cases amplify thermo inconsistency, pressure/thermal BC mismatch, local high-gradient mesh weakness, timestep sensitivity, and brittle steady-startup numerics

## 5) Multiphase interface flow
Primary nodes:
- `p-vs-p_rgh-confusion`
- `multiphase-interface-initialization-mismatch`
- `courant-driven-transient-instability`
- `mesh-quality-driven-instability`
- `critical-region-local-mesh-hotspot`
- `parallel-only-failure`
- `processor-count-sensitive-parallel-failure`
- `processor-boundary-field-inconsistency`
- `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- `wrong-solver-family-selection`
- `patch-name-boundary-mismatch`

Typical rationale:
- multiphase startup is especially sensitive to pressure convention, interface initialization, local interface-region mesh weakness, transient stability control, and decomposition sensitivity when interfaces are parallelized

## 6) Reacting / combustion flow
Primary nodes:
- `thermo-chemistry-package-inconsistency`
- `wrong-solver-family-selection`
- `reacting-startup-coupling-too-stiff`
- `courant-driven-transient-instability`
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`
- `turbulence-field-startup-mismatch`
- `patch-name-boundary-mismatch`

Typical rationale:
- reacting cases strongly couple thermo, chemistry, turbulence, startup control, and local high-gradient hotspot behavior; wrong branch selection is especially costly, and startup stiffness often needs explicit staged handling

## Routing rule for agents
When a user asks for troubleshooting help:
1. identify the closest scenario template
2. load the primary node set above
3. classify the symptom more precisely
4. choose the top 1–3 nodes that match the observed symptom
5. only then expand to wider knowledge-base search
