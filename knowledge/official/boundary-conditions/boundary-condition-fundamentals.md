# Boundary Condition Fundamentals

id: official-boundary-condition-fundamentals
problem_class: setup
confidence: high
source_refs:
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-field-file-format

## Why this note exists

Boundary conditions are one of the most common sources of OpenFOAM setup failure and nonphysical results. Many cases do not fail because the solver is wrong, but because the field file entries at the boundaries are mathematically inconsistent, physically unreasonable, or mismatched to the chosen solver family. A reliable agent must understand boundary conditions as part of the equation setup, not as decorative case metadata.

## What a boundary condition is doing

A boundary condition tells OpenFOAM how a solved field behaves on a patch. In practice, it supplies one of the ingredients needed to close the discretized equations at the domain boundary.

For a given field, a patch entry is not just a label like `fixedValue` or `zeroGradient`; it is a statement about what the solver should assume at that boundary for that variable.

## Where boundary conditions live

Boundary conditions are usually set in field files under `0/`, for example:

- `0/U`
- `0/p`
- `0/p_rgh`
- `0/T`
- turbulence fields such as `0/k`, `0/epsilon`, `0/omega`, `0/nut`

Each field file contains a `boundaryField` section. The patch names inside that section must match the patch names defined by the mesh boundary description.

## Core practical distinction: value-like vs gradient-like specification

A very useful first-pass mental model is:

- `fixedValue`: prescribe the field value on the boundary
- `zeroGradient`: prescribe zero normal gradient

This is not the full boundary-condition universe, but it is the cleanest baseline for understanding how many practical choices work.

Examples:

- Velocity inlet often uses value-type specification
- Pressure outlet often uses gradient-type specification
- Wall thermal conditions may be value-based, flux-based, or mixed depending on the physics

## Pressure-velocity coupling matters

Boundary conditions cannot be chosen field-by-field in isolation. A velocity condition and a pressure condition on the same physical boundary must make sense together.

Typical examples:

- If velocity is fixed at an inlet, pressure often needs a complementary treatment instead of also being over-constrained.
- If pressure is fixed at an outlet, velocity often uses a gradient-style outlet treatment.

Many startup failures or unphysical recirculation patterns come from over-constraining or under-constraining coupled fields.

## Solver-family dependence

Boundary-condition correctness depends on the solver family.

Examples:

- Incompressible cases often use `p`
- Buoyant or free-surface-related formulations may use `p_rgh`
- Turbulent runs require model-field boundary conditions in addition to primary variables
- Compressible or thermal cases add temperature and thermo-sensitive fields

A boundary setup that is correct in one tutorial can be structurally wrong in another solver family even if the geometry looks similar.

## Turbulence boundary conditions are not optional details

When turbulence is enabled, the primary flow variables are not enough. The case may also require physically and mathematically consistent boundary conditions for fields such as:

- `k`
- `epsilon`
- `omega`
- `nut`
- `nuTilda`

A frequent anti-pattern is copying `U` and `p` carefully while leaving turbulence fields inconsistent, defaulted, or copied from the wrong model family.

## Practical review checklist

Before running a case, verify:

1. Patch names in `boundaryField` exactly match the mesh boundary patches.
2. The field set under `0/` matches the selected solver and model set.
3. Boundary conditions for coupled variables are complementary, not contradictory.
4. Turbulence-enabled cases include consistent turbulence field boundary conditions.
5. Any use of `p_rgh` vs `p` is solver-family correct.
6. Wall, inlet, outlet, symmetry, and empty patches are used in physically sensible places.
7. Boundary conditions have not been copied blindly from a different tutorial family.

## Common failure modes

- Patch name mismatch between mesh and `boundaryField`
- Fixing too many coupled variables on one boundary
- Using `p` boundary logic in a `p_rgh` case
- Forgetting turbulence field boundary conditions
- Using wall-type conditions on a non-wall patch
- Reusing incompressible BC patterns in compressible or buoyant cases

## Anti-patterns

- Thinking of boundary conditions as patch labels rather than equation constraints
- Copying BCs from a tutorial without checking solver and physics compatibility
- Debugging numerics for hours before checking if the BC set is structurally inconsistent
- Treating turbulence-field BCs as secondary afterthoughts

## Recommendation

- Review boundary conditions as a coupled system, not one field at a time.
- Start with the solver family, then identify the required field set, then check patch-by-patch consistency.
- Use the simplest physically correct baseline first; only add advanced mixed or specialized conditions when the case needs them.
- Classify boundary-condition errors as setup-class failures before touching numerics.

## Rationale

- Many non-convergent or unphysical cases are structurally doomed at the boundary-condition layer.
- Boundary conditions encode the problem statement at the domain edge, so they should be treated as part of model formulation.
- A disciplined BC review dramatically reduces false troubleshooting branches.

## Applicability limits

- Specialized solvers may require boundary-condition types not covered by this baseline note.
- Exact recommended BC patterns depend on geometry, solver family, turbulence model, and physics.
- Advanced coupled and multiphase cases need more detailed case-specific treatment beyond fixedValue/zeroGradient fundamentals.
