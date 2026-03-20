# Tutorial Pattern — Premixed Combustion Baseline

id: tutorial-premixed-combustion-baseline-pattern
problem_class: combustion
confidence: high
source_refs:
- official-openfoam-tutorial-premixed-combustion-xifoam
- official-openfoam-tutorial-catalog
- official-openfoam-xifoam-guide
- official-openfoam-thermophysical-properties

## Representative solver family

Use `XiFoam` as the primary tutorial anchor for premixed turbulent combustion in this pass.

## Steady vs transient intent

Treat startup as transient or cautiously staged first. Premixed ignition and progress-variable formation are rarely a good place for an aggressive first solve.

## Required `0/` fields

- `U`
- pressure field expected by the premixed branch
- `T`
- premixed progress-variable or burned-fraction fields required by the chosen branch
- flame-wrinkling fields required by the chosen branch

## Key `constant/` dictionaries

- `thermophysicalProperties`
- combustion-model dictionary required by the premixed branch
- `turbulenceProperties` when turbulence is enabled
- `polyMesh`

## Key `system/` dictionaries

- `controlDict`
- `fvSchemes`
- `fvSolution`

## Initialization guidance

- keep ignition and premixed progress fields explicit from the start
- compare against a premixed tutorial lineage before improvising field names or combustion-model switches
- keep the first launch conservative until the flame structure behaves coherently

## Stability risks

- missing or mismatched premixed progress-variable fields
- copying a nonpremixed or generic reacting structure into a premixed case
- ignition defined loosely enough that the run starts from an impossible premixed state

## Debug priority order

1. verify the premixed branch and required fields
2. verify ignition and progress-variable initialization
3. verify thermo and BC coherence as one coupled premixed system
4. only then escalate into broader reacting stiffness review

## Applicability limits

- this pattern is a premixed baseline, not a universal model-choice rule
- partially premixed recirculating combustors may share this lineage but need extra return-state checks
