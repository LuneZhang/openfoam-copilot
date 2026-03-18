# turbulenceProperties Activation Basics

id: official-turbulenceProperties-activation-basics
problem_class: turbulence
confidence: high
source_refs:
- official-openfoam-user-guide-turbulence-properties
- official-openfoam-user-guide-solver-selection
- official-openfoam-tutorial-conventions

## Why this note exists

Turning turbulence on in OpenFOAM is not a single switch. It changes expected fields, model dictionaries, wall treatment assumptions, and startup behavior. Agents need a clean activation mental model so they can distinguish a real turbulence setup from a case that merely copied a tutorial fragment.

## What `turbulenceProperties` usually does

This dictionary declares whether the case is laminar or turbulence-enabled and identifies the modeling family used for momentum closure.

In practice it answers:
- is the run laminar, RANS, LES, or another supported mode?
- which turbulence model class is active?
- which additional fields and near-wall expectations follow from that choice?

## Activation consequences

When a case moves from laminar to turbulence-enabled, the review surface expands:
- extra fields may be required under `0/`
- wall boundary conditions may need model-aware treatment
- `constant/` now carries more model semantics
- startup numerics may need more conservative choices
- tutorial lineage becomes more important because model-specific field sets differ

## Practical review order

1. confirm the solver family is appropriate before touching turbulence details
2. inspect `turbulenceProperties` to see whether the case is actually laminar, RANS, or LES
3. verify all model-required fields exist in `0/`
4. verify wall and patch treatment is coherent with the chosen model family
5. only then review numerics and convergence behavior

## Typical failure modes

- enabling turbulence without adding required model fields
- copying `k`/`epsilon` or `k`/`omega` files from the wrong tutorial family
- using near-wall treatment inconsistent with the mesh resolution strategy
- treating LES and RANS as interchangeable because both are "turbulence"
- debugging residuals for hours before noticing the turbulence mode is mismatched to the copied field set

## Anti-patterns

- toggling turbulence mode as a generic convergence trick
- assuming wall functions are automatically correct for any wall mesh
- inheriting turbulence settings from a tutorial with unrelated geometry or Reynolds regime

## Recommendation

- Treat `turbulenceProperties` as a gateway dictionary: once it changes, re-check fields, BCs, and mesh assumptions together.
- Keep future templates explicit about which extra fields each turbulence family introduces.
- Use official tutorial lineage to validate field-set expectations before applying community heuristics.

## Rationale

- Turbulence setup errors often masquerade as numerics problems.
- The dictionary itself is small, but it changes the meaning of large parts of the case.
- Clear activation logic helps agents separate laminar baseline review from turbulence-specific troubleshooting.

## Applicability limits

- Exact syntax and supported models differ across OpenFOAM variants and versions.
- Final model choice depends on physics goals and mesh resolution, not just dictionary availability.
