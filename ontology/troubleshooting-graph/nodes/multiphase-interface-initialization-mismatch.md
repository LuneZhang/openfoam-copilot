# Troubleshooting Node — Multiphase Interface Initialization / Phase-Topology Mismatch

id: multiphase-interface-initialization-mismatch
symptom: A multiphase case destabilizes immediately or behaves unphysically because the initial phase layout, phase fractions, gravity/pressure framing, or interface topology appear inconsistent with the intended physical problem.

probable_causes:
- the interface topology is not initialized to match the intended physical phase arrangement
- phase fields were added onto a single-phase baseline without rebuilding the case structure around the interface problem
- the chosen pressure convention and gravity framing are inconsistent with the multiphase branch
- opening / outlet / wall BCs for pressure and phase fields are individually legal but inconsistent as an interface system
- the initial phase distribution creates nonphysical regions, trapped patches, or impossible startup geometry before numerics even get a fair chance

first_checks:
- confirm the solver family and required phase-field set are correct for the intended multiphase problem class
- inspect the initial interface/phase topology directly instead of assuming the `alpha.*` fields are merely bookkeeping
- confirm pressure convention (`p` vs `p_rgh` where relevant) and gravity setup are coherent with the multiphase branch
- review pressure, phase-fraction, and opening BCs together as one coupled interface system
- compare the case against the nearest official multiphase tutorial family rather than against a single-phase template with added fields

deeper_checks:
- inspect whether instability begins before meaningful interface transport develops, which often signals structural initialization mismatch rather than later timestep failure
- separate wrong interface topology from local interface-region mesh fragility that merely makes a plausible topology hard to transport
- verify that the initial interface location does not create immediate conflict with geometry, patch roles, or hydrostatic framing
- if the case is only problematic in parallel, distinguish true initialization mismatch from decomposition-fragmented interface sensitivity

likely_fixes:
- rebuild the initial phase topology so it matches the intended physical arrangement explicitly
- replace borrowed single-phase assumptions with a multiphase-native tutorial baseline
- correct pressure/gravity/phase-field coupling before retuning timestep or numerics
- repair interface-related BC sets as a coupled system rather than patching one field at a time

escalation_path:
- if the main issue is pressure convention itself, route to `p-vs-p_rgh-confusion`
- if the main issue is local mesh fragility near the interface, route to `critical-region-local-mesh-hotspot`
- if serial is fine but parallel exposes interface fragmentation, route to `processor-boundary-field-inconsistency` or `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- if the topology is plausible but timestep/interface transport is too aggressive, route to `courant-driven-transient-instability`

source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-solver-selection
- official-openfoam-hydrostatic-pressure-effects
- official-openfoam-field-file-format
- official-openfoam-user-guide-boundary-conditions

confidence: medium
notes:
- This node is for structural multiphase mis-initialization, not for every unstable free-surface run.
- Many multiphase startups fail before numerics tuning because the interface problem is posed incorrectly from the first time step.
