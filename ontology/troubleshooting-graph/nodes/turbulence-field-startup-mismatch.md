# Troubleshooting Node — Turbulence Field Startup Mismatch

id: turbulence-field-startup-mismatch
symptom: A turbulent case starts badly, diverges, or shows clearly inconsistent near-wall / turbulence-field behavior soon after launch.

probable_causes:
- missing required turbulence fields for the chosen model family
- mixed field set from incompatible turbulence branches
- wall treatment inconsistent with the selected turbulence model and mesh strategy
- turbulence fields copied from a tutorial with different physical assumptions

first_checks:
- confirm turbulence is intentionally enabled
- verify the required turbulence fields exist under `0/`
- verify the field family matches the selected turbulence model branch
- inspect wall and inlet/outlet BCs for turbulence quantities

deeper_checks:
- compare against the nearest official turbulent tutorial family
- check whether near-wall mesh and wall treatment assumptions are compatible
- separate turbulence startup issues from more basic BC or mesh problems

likely_fixes:
- restore a coherent turbulence field set for the chosen model branch
- fix wall-function or near-wall BC mismatches
- simplify startup and validate the baseline turbulent case before refinement

escalation_path:
- if the case remains unstable, branch into wall-treatment/mesh-resolution mismatch or general BC/numerics instability

source_refs:
- official-openfoam-user-guide-turbulence-properties
- official-openfoam-turbulence-model-overview
- official-openfoam-tutorial-catalog

confidence: high
notes:
- Do not use turbulence-model tuning as a substitute for fixing a structurally wrong field set.
