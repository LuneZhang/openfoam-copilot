# transportProperties Basics

id: official-transportProperties-basics
problem_class: setup
confidence: high
source_refs:
- official-openfoam-user-guide-transport-properties
- official-openfoam-tutorial-conventions

## Why this note exists

`transportProperties` is one of the easiest files to copy blindly and one of the easiest ways to smuggle the wrong physical assumptions into a case. Agents need to treat it as a physics-definition dictionary, not as a harmless constant bag.

## What this dictionary usually controls

Depending on solver family and distribution, `transportProperties` commonly holds transport-model information such as:
- kinematic or dynamic viscosity assumptions
- Newtonian vs non-Newtonian transport model choice
- phase-specific transport coefficients in simpler multiphase contexts
- other material transport parameters expected by the selected solver family

The exact contents vary. The key point is that this file often encodes whether momentum transport is being modeled in a physically coherent way for the chosen solver.

## Review rule

Never review `transportProperties` in isolation. Always pair it with:
1. selected solver/application
2. incompressible vs compressible framing
3. turbulence model activation state
4. tutorial lineage or reference case family

A file that looks syntactically valid may still be semantically wrong for the case.

## Common review questions

- Does the case actually use `transportProperties`, or is transport defined elsewhere for this solver family?
- Are the declared transport coefficients in the right units and magnitude range?
- Is the transport model class compatible with the intended fluid behavior?
- Was this file copied from a tutorial with very different Reynolds number or material properties?
- If turbulence is enabled, does the laminar transport definition still make sense as the molecular baseline?

## Failure modes

- copying air properties into a liquid-flow case
- confusing dynamic and kinematic viscosity conventions
- using an incompressible-style transport dictionary in a thermo-driven case that expects another property structure
- assuming turbulence settings replace the need for correct molecular transport values

## Anti-patterns

- treating viscosity as a tuning knob to make convergence easier
- accepting a tutorial’s transport values without checking dimensional meaning
- reviewing turbulence before checking whether baseline transport is even plausible

## Recommendation

- Validate `transportProperties` immediately after confirming solver family.
- Compare material values against the intended working fluid, not against whatever tutorial was copied.
- Record solver-family-specific property-file expectations in future templates.

## Rationale

- Wrong transport assumptions can produce misleadingly stable but physically useless runs.
- Many later turbulence and numerics decisions depend on the baseline transport framing.
- This dictionary is low-volume but high-leverage in setup review.

## Applicability limits

- Some solver families use other property dictionaries as the primary thermo/transport source.
- Exact keywords vary across OpenFOAM distributions and versions.
