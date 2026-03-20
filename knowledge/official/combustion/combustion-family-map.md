# Combustion Family Map

id: official-combustion-family-map
problem_class: combustion
confidence: high
source_refs:
- official-openfoam-user-guide-solver-selection
- official-openfoam-xifoam-guide
- official-openfoam-reactingfoam-guide
- official-openfoam-firefoam-guide
- official-openfoam-sprayfoam-guide

## Why this note exists

The repository used to treat reacting flow as one broad branch. That was enough for generic routing, but it hid real differences between premixed, diffusion-flame, buoyant-fire, recirculating-combustor, and spray-combustion cases. Agents need a narrow first-pass map before they choose nodes.

## Active family set

Use exactly these five families in this pass:

1. `premixed-combustion-baseline`
2. `nonpremixed-diffusion-flame`
3. `buoyant-fire-compartment`
4. `partially-premixed-recirculating-combustor`
5. `spray-combustion`

Keep `reacting-combustion-flow-generic` as the active parent and fallback when the case is reacting but not yet narrow enough.

## Primary differentiators

### Premixed combustion baseline

Use when the reactants enter as a mixed combustible stream and the main startup question is whether the premixed progress-variable branch is structurally coherent.

### Nonpremixed diffusion flame

Use when fuel and oxidizer enter as separate streams and stream composition plus reverse-flow state treatment matter before later chemistry tuning.

### Buoyant fire compartment

Use when fire, buoyancy, ventilation openings, and modified-pressure framing dominate the setup.

### Partially premixed recirculating combustor

Use when the case has a premixed-like flame branch but the first structural risk is the recirculating return state, pilot stream, or flameholder-region setup.

### Spray combustion

Use when parcels, injection timing, and carrier-phase thermo coupling dominate the first startup checks.

## Safe fallback rule

If the solver lineage or case statement is still unclear, do not force one narrow combustion family too early. Stay on `reacting-combustion-flow-generic`, verify the reacting structure, then narrow only when the case evidence supports it.

## Applicability limits

- This map is intentionally narrow.
- It does not add engine-combustion taxonomy.
- It does not claim every reacting case fits one of these five families.
