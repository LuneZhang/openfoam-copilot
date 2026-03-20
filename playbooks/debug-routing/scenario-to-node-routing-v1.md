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

## 7) Premixed combustion baseline
Primary nodes:
- `premixed-ignition-or-flame-speed-model-mismatch`
- `reacting-startup-coupling-too-stiff`
- `thermo-chemistry-package-inconsistency`
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

Typical rationale:
- premixed XiFoam-like cases fail early when ignition, progress-variable, or flame-wrinkling structure is copied loosely; once the family is already identified, that narrow branch is usually more informative than generic solver-family mismatch

## 8) Nonpremixed diffusion flame
Primary nodes:
- `nonpremixed-mixture-fraction-or-stoichiometric-inlet-mismatch`
- `outlet-backflow-role-confusion`
- `thermo-chemistry-package-inconsistency`
- `reacting-startup-coupling-too-stiff`
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

Typical rationale:
- separated-stream combustion usually fails first on fuel and oxidizer stream definition, species BC coherence, or reverse-flow state treatment before it becomes a pure chemistry-stiffness problem

## 9) Buoyant fire compartment
Primary nodes:
- `firefoam-ventilation-radiation-or-hrr-coupling-mismatch`
- `buoyant-pressure-anchor-reference-mismatch`
- `outlet-backflow-role-confusion`
- `courant-driven-transient-instability`
- `critical-region-local-mesh-hotspot`

Typical rationale:
- fireFoam-style compartment cases are branch-shaped by buoyancy, `p_rgh`, ventilation openings, and ambient return-state assumptions, so opening and reference-state review usually beats broad reacting numerics tuning

## 10) Partially premixed recirculating combustor
Primary nodes:
- `recirculating-combustor-flame-holding-or-backflow-mismatch`
- `outlet-backflow-role-confusion`
- `premixed-ignition-or-flame-speed-model-mismatch`
- `reacting-startup-coupling-too-stiff`
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

Typical rationale:
- recirculating combustors often look like generic reacting stiffness until the returning mixture state, pilot stream, or flameholder-region setup is checked explicitly

## 11) Spray combustion
Primary nodes:
- `spray-injection-evaporation-coupling-startup-fragility`
- `reacting-startup-coupling-too-stiff`
- `thermo-chemistry-package-inconsistency`
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

Typical rationale:
- sprayFoam-style runs often destabilize at injection onset because parcel, injection, and carrier-phase structure are wrong long before a generic reacting startup branch becomes the best explanation

## Routing rule for agents
When a user asks for troubleshooting help:
1. identify the closest scenario template
2. load the primary node set above
3. classify the symptom more precisely
4. choose the top 1–3 nodes that match the observed symptom
5. only then expand to wider knowledge-base search
