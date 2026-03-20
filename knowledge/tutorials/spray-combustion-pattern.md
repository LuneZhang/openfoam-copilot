# Tutorial Pattern — Spray Combustion

id: tutorial-spray-combustion-pattern
problem_class: combustion
confidence: high
source_refs:
- official-openfoam-tutorial-spray-combustion-sprayfoam
- official-openfoam-tutorial-catalog
- official-openfoam-sprayfoam-guide
- official-openfoam-thermophysical-properties

## Representative solver family

Use `sprayFoam` as the primary tutorial anchor for spray-combustion routing in this pass.

## Steady vs transient intent

Treat startup as transient first, especially across injection onset and early parcel-cloud formation.

## Required `0/` fields

- `U`
- pressure field expected by the spray branch
- `T`
- carrier-phase species or reacting fields required by the chosen branch

## Key `constant/` dictionaries

- `thermophysicalProperties`
- parcel or injection dictionaries required by the spray branch
- turbulence dictionaries when enabled
- `polyMesh`

## Key `system/` dictionaries

- `controlDict`
- `fvSchemes`
- `fvSolution`

## Initialization guidance

- keep injector timing, parcel properties, and carrier-phase reference state explicit from the first run
- compare injection dictionaries against the nearest spray tutorial family before modifying breakup or evaporation details
- watch whether instability begins exactly when injection starts

## Stability risks

- injection dictionaries structurally mismatched to the carrier-phase branch
- parcel temperature or diameter state inconsistent with the intended injector setup
- a generic reacting template reused without the spray-specific parcel layer

## Debug priority order

1. verify parcel and injection structure
2. verify carrier-phase thermo coherence
3. verify startup controls around injection onset
4. only then widen to generic reacting stiffness or mesh review

## Applicability limits

- `sprayFoam` details are distribution-sensitive and version-sensitive
- this pattern does not replace exact branch documentation for parcel and submodel choices
