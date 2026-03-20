# Tutorial Pattern — Partially Premixed Recirculating Combustor

id: tutorial-partially-premixed-recirculating-combustor-pattern
problem_class: combustion
confidence: medium
source_refs:
- official-openfoam-tutorial-premixed-combustion-xifoam
- official-openfoam-tutorial-catalog
- official-openfoam-xifoam-guide
- official-openfoam-docs-inletOutlet-backflow

## Representative solver family

Use `XiFoam` as the primary tutorial anchor in this pass, but treat recirculation and return-state structure as the extra narrowing step beyond a plain premixed baseline.

## Steady vs transient intent

Treat startup as transient or staged first. Pilot stabilization and recirculation-zone formation usually matter before any aggressive target solve.

## Required `0/` fields

- `U`
- pressure field expected by the chosen branch
- `T`
- premixed progress-variable or related premixed fields
- any extra species fields required by pilot or secondary streams

## Key `constant/` dictionaries

- `thermophysicalProperties`
- combustion-model dictionary required by the branch
- `turbulenceProperties` when turbulence is enabled
- `polyMesh`

## Key `system/` dictionaries

- `controlDict`
- `fvSchemes`
- `fvSolution`

## Initialization guidance

- define pilot, main stream, and recirculating return state explicitly
- treat reverse-flow-capable outlets as part of the combustor setup, not as generic exhaust
- compare flameholder or recirculation-region structure against the nearest premixed tutorial lineage before widening the model family

## Stability risks

- returning hot products or mixed reactants are left undefined at reverse-flow patches
- a plain premixed template is reused without the extra recirculation-state audit
- pilot and main streams are structurally inconsistent

## Debug priority order

1. verify return-state and reverse-flow treatment
2. verify pilot and main-stream coherence
3. verify premixed branch structure
4. only then widen into generic reacting stiffness review

## Applicability limits

- this pattern is a justified extension of the premixed tutorial lineage, not a claim that every recirculating combustor should use the same solver branch
