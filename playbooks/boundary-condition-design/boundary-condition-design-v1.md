# Boundary Condition Design v1

## Goal
Provide a first-pass workflow for designing and reviewing OpenFOAM boundary conditions.

## Step 1 — Start from physical meaning, not dictionary names
For each boundary patch, identify:
- what the patch physically represents
- which variables are physically known there
- which variables should respond rather than be directly imposed

If this is unclear, stop. A BC set built on fuzzy physical meaning is usually unstable or misleading.

## Step 2 — Identify the field set implied by the solver family
Before assigning any patch entries, determine which fields are active:
- primary flow fields
- pressure variable form (`p` or `p_rgh` where applicable)
- turbulence fields
- thermal fields
- phase/species fields where relevant

## Step 3 — Design BCs as a coupled set
Do not design `U`, pressure, turbulence, and thermal BCs independently.
For each patch, ask:
- if velocity is prescribed, how should pressure behave?
- if pressure is prescribed, what is the velocity implication?
- if turbulence is enabled, what must happen to `k`, `epsilon`, `omega`, `nut`, etc.?
- if buoyancy/thermal effects matter, what additional field constraints are required?

## Step 4 — Validate patch semantics
Check that each patch is correctly classified as one of the intended physical roles, such as:
- inlet
- outlet
- wall
- symmetry/symmetryPlane
- empty (for reduced-dimensional setups)

Misclassified patch semantics often create hidden setup errors.

## Step 5 — Prefer the simplest physically correct baseline
When bootstrapping a case:
- choose the simplest BC set that is physically coherent
- avoid exotic mixed/specialized conditions unless the problem clearly requires them
- get the baseline stable first, then refine

## Common design errors
- over-constraining pressure and velocity simultaneously
- forgetting turbulence-field BCs
- copying BCs from a different solver family
- using `p` logic where `p_rgh` logic is required
- applying wall logic to non-wall patches
- using reduced-dimensional patch types incorrectly

## Review checklist
1. Do patch names match the mesh boundary names exactly?
2. Is each patch physically interpreted correctly?
3. Are primary variable BCs complementary rather than contradictory?
4. Are turbulence and thermal fields covered where required?
5. Is the solver family consistent with the chosen pressure variable convention?
6. Was any BC copied from a tutorial with different physics or geometry assumptions?

## Recommendation
- Treat BC design as one of the highest-priority setup tasks.
- If the case diverges immediately, revisit BC structure before changing numerics.
- Record BC intent patch-by-patch in future scenario templates.

## Recommended Scenario Families

- `incompressible-laminar-internal-flow`
- `incompressible-rans-external-aerodynamics`
- `buoyant-natural-convection-room-scale`
- `compressible-thermo-flow-generic`
- `multiphase-interface-flow-generic`

## Primary Troubleshooting Node Handoffs

- `patch-name-boundary-mismatch`
- `p-vs-p_rgh-confusion`
- `buoyant-pressure-anchor-reference-mismatch`
- `turbulence-field-startup-mismatch`
- `turbulence-field-family-patch-role-mismatch`
- `wrong-solver-family-selection`
