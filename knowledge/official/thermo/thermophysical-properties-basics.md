# thermophysicalProperties Basics

id: official-thermophysical-properties-basics
problem_class: thermo
confidence: high
source_refs:
- official-openfoam-thermophysical-properties
- official-openfoam-compressible-setup-guidance

## Why this note exists

Thermophysical setup is a major failure source in compressible, heat-transfer, buoyant, and reacting cases. Agents often focus on solver and numerics while underestimating how strongly thermophysical package consistency shapes case viability.

## Core principle
`thermophysicalProperties` is not a side dictionary. It defines how material properties and thermo relationships are represented. If this layer is inconsistent with the chosen solver family or intended physics, the case may fail even when numerics look conservative.

## What this dictionary controls conceptually
Depending on solver family and distribution, thermophysical setup typically governs:
- equation of state assumptions
- transport-property behavior
- energy/enthalpy/internal-energy framing
- species/mixture treatment where applicable
- temperature-dependent property behavior

## Practical meaning for agents
When a case involves compressibility, buoyancy, strong thermal coupling, or reacting flow, the agent should explicitly verify:
1. whether thermo is actually part of the governing physics
2. whether the chosen solver family expects a thermo package
3. whether the property model family is internally coherent
4. whether field setup and boundary conditions match the thermo assumptions

## Common setup risks
- copying a thermo dictionary from a mismatched tutorial family
- treating a compressible or thermal case like an incompressible one with just an extra temperature field
- mixing property assumptions that do not belong together
- using the wrong primary thermal framing for the intended solver workflow

## Practical review checklist
1. Confirm that the selected solver family really matches the intended thermo/energy behavior.
2. Confirm that `thermophysicalProperties` exists where the solver family requires it.
3. Confirm that thermal fields and BCs align with the thermo package assumptions.
4. Confirm that the intended physical material model is represented with a coherent set of property choices.
5. If using a tutorial as a baseline, verify that its thermo assumptions transfer to the new case.

## Common failure symptoms linked to thermo inconsistency
- nonphysical temperature evolution
- density behavior that does not match the intended regime
- repeated instability that survives simple numerics damping
- apparent BC problems that are actually property-model mismatches

## Recommendation
- Treat thermo review as a first-class setup step in thermal, compressible, buoyant, and reacting cases.
- Use official tutorial families as anchors when uncertain.
- If thermo consistency is doubtful, resolve that before aggressive numerics tuning.

## Applicability limits
- Exact dictionary structure varies by solver family and OpenFOAM distribution.
- This note provides a review framework, not a line-by-line replacement for official thermo documentation.
