# Tutorial Pattern — Nonpremixed Diffusion Flame

id: tutorial-nonpremixed-diffusion-flame-pattern
problem_class: combustion
confidence: high
source_refs:
- official-openfoam-tutorial-nonpremixed-diffusion-reactingfoam
- official-openfoam-tutorial-catalog
- official-openfoam-reactingfoam-guide
- official-openfoam-thermophysical-properties

## Representative solver family

Use `reactingFoam` as the primary tutorial anchor for nonpremixed and diffusion-flame routing in this pass.

## Steady vs transient intent

Treat startup as transient or staged first, especially while fuel and oxidizer streams are still being proven structurally coherent.

## Required `0/` fields

- `U`
- pressure field expected by the reacting branch
- `T`
- required species fields for fuel, oxidizer, and products

## Key `constant/` dictionaries

- `thermophysicalProperties`
- chemistry or reacting dictionaries required by the chosen branch
- `turbulenceProperties` when turbulence is enabled
- `polyMesh`

## Key `system/` dictionaries

- `controlDict`
- `fvSchemes`
- `fvSolution`

## Initialization guidance

- keep fuel and oxidizer stream states explicit rather than hiding them behind generic inlet wording
- compare species BCs and stream temperatures against the nearest reacting tutorial family
- verify reverse-flow patches have meaningful return-state treatment before blaming chemistry alone

## Stability risks

- species BC mismatch between fuel and oxidizer streams
- undefined return-state values at recirculating outlets or openings
- thermo structure copied from a broad reacting template without separated-stream review

## Debug priority order

1. verify separated-stream species and temperature structure
2. verify reverse-flow and outlet treatment
3. verify thermo and chemistry package coherence
4. only then escalate into generic reacting startup stiffness

## Applicability limits

- this pattern is for diffusion-flame framing, not fully premixed or spray branches
