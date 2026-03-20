# Tutorial Pattern — Buoyant Fire Compartment

id: tutorial-buoyant-fire-compartment-pattern
problem_class: combustion
confidence: high
source_refs:
- official-openfoam-tutorial-buoyant-fire-compartment-firefoam
- official-openfoam-firefoam-guide
- official-openfoam-hydrostatic-pressure-effects
- official-openfoam-tutorial-catalog

## Representative solver family

Use `fireFoam` as the primary tutorial anchor for buoyant fire and compartment-fire routing in this pass.

## Steady vs transient intent

Treat the branch as transient first. Fire growth, buoyancy, and opening exchange are part of the physical problem, not a late refinement.

## Required `0/` fields

- `U`
- `p_rgh`
- `T`
- species or fire fields required by the chosen branch

## Key `constant/` dictionaries

- `g`
- `thermophysicalProperties`
- combustion or fire-model dictionaries required by the branch
- `radiationProperties` when radiation is enabled
- `polyMesh`

## Key `system/` dictionaries

- `controlDict`
- `fvSchemes`
- `fvSolution`

## Initialization guidance

- keep the opening and ambient reference state explicit at startup
- verify the modified-pressure framing before tuning ventilation numerics
- compare the fire source and ventilation layout against the nearest compartment-fire tutorial lineage

## Stability risks

- wrong `p_rgh` framing or reference state
- openings treated as pure outflow when hot gases can recirculate
- buoyancy, fire source, and ambient state copied from different tutorial branches

## Debug priority order

1. verify `p_rgh`, gravity, and ambient reference framing
2. verify opening backflow and return-state treatment
3. verify fire source and thermo coherence
4. only then widen to generic reacting instability

## Applicability limits

- `fireFoam` details are distribution-sensitive and version-sensitive
- this pattern is not a replacement for exact tutorial or solver documentation
