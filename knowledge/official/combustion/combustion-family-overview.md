# Combustion Family Overview

id: official-combustion-family-overview
problem_class: combustion
confidence: high
source_refs:
- official-openfoam-user-guide-solver-selection
- official-openfoam-xifoam-guide
- official-openfoam-reactingfoam-guide
- official-openfoam-firefoam-guide
- official-openfoam-sprayfoam-guide

## Why this note exists

The runtime spine now separates five narrow combustion families from the old generic reacting branch. Agents need a compact official overview that explains what each family is for before later routing or troubleshooting becomes narrower.

## Active family set

Use exactly these five narrow combustion families in this pass:

1. `premixed-combustion-baseline`
2. `nonpremixed-diffusion-flame`
3. `buoyant-fire-compartment`
4. `partially-premixed-recirculating-combustor`
5. `spray-combustion`

Keep `reacting-combustion-flow-generic` as the parent fallback when the case is clearly reacting but not yet narrow enough for one specialized family.

## Family summary

### Premixed combustion baseline

Anchor this family to `XiFoam`-style premixed setup where ignition, flame-speed modeling, and progress-variable framing matter before later tuning.

### Nonpremixed diffusion flame

Anchor this family to `reactingFoam` diffusion-flame setup where separated stream composition, stoichiometric framing, and reverse-flow state treatment matter early.

### Buoyant fire compartment

Anchor this family to `fireFoam`-style buoyant fire setup where openings, ventilation, modified-pressure framing, and ambient return state are structurally central.

### Partially premixed recirculating combustor

Anchor this family to premixed-capable `XiFoam`-style setups with recirculation, flame holding, pilot/return state, and backflow-sensitive combustor framing.

### Spray combustion

Anchor this family to `sprayFoam`-style setups where injector structure, parcels, evaporation, and carrier-phase startup coupling dominate the first checks.

## Applicability limits

- This overview is intentionally narrow.
- It does not add engine combustion taxonomy in this pass.
- It does not replace the generic reacting template when the family evidence is still broad or ambiguous.
