# fireFoam and sprayFoam Scope Sensitivity

id: official-firefoam-sprayfoam-scope-sensitivity
problem_class: combustion
confidence: high
source_refs:
- official-openfoam-firefoam-guide
- official-openfoam-sprayfoam-guide
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-solver-selection

## Why this note exists

`fireFoam` and `sprayFoam` are useful combustion anchors, but they are also the most distribution-sensitive and version-sensitive families in this expansion wave. Agents should not copy them across OpenFOAM variants as casually as a generic `reactingFoam` baseline.

## Practical rule

When a case points to `fireFoam` or `sprayFoam`, verify the exact distribution and documentation version before reusing dictionary structure or tutorial assumptions.

## What to audit first

1. confirm the exact solver name exists in the target distribution
2. compare the case against the nearest tutorial family from the same documentation lineage
3. verify the required combustion, parcel, radiation, buoyancy, or opening dictionaries are present for that branch
4. treat missing or renamed branch-specific dictionaries as a structural issue, not a late numerics issue

## Safe reuse boundary

- Reuse branch ideas only after the target distribution confirms the same solver family and dictionary model.
- Keep family-specific notes tied to their source IDs in the runtime source catalog.
- If distribution certainty is weak, fall back to the generic reacting template while gathering evidence.

## Applicability limits

- This note is about branch selection and source reuse discipline.
- It is not a complete solver manual for either family.
