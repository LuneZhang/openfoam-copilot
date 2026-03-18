# Troubleshooting Node — Turbulence Field Family / Patch-Role Mismatch

id: turbulence-field-family-patch-role-mismatch
symptom: A RANS case launches with turbulence enabled but diverges early, shows suspicious near-wall turbulence behavior, or behaves as if turbulence quantities were copied from the wrong model family or assigned to the wrong patch roles.

probable_causes:
- the case mixes `k-epsilon` and `k-omega` style field families or wall treatments
- wall patches use turbulence BCs that do not match the chosen model family or wall-resolution strategy
- inlet/opening patches carry turbulence quantities copied from another tutorial family without matching the intended turbulence assumptions
- turbulence fields look syntactically complete under `0/` but their patch roles are physically inconsistent
- the case uses a wall-sensitive turbulence family while leaving free-stream / inlet turbulence quantities implausible or under-specified

first_checks:
- identify the active turbulence family first and verify that the field set under `0/` belongs to that family only
- inspect wall patches to confirm the turbulence BC types match the chosen family and wall-treatment strategy
- inspect inlet, outlet, and far-field patches to verify turbulence quantities are physically plausible for those patch roles rather than copied blindly
- check whether the run is being blamed on numerics before turbulence field family and patch-role consistency have been reviewed
- compare the patch-level turbulence treatment against the nearest official turbulent tutorial family

deeper_checks:
- separate family mismatch from simpler cases where the turbulence fields are merely missing altogether
- inspect whether instability begins in near-wall cells, at inflow/opening patches, or globally across the domain
- check whether the selected turbulence family is already questionable for the mesh / y-plus strategy, making the BC set brittle even if syntax is valid
- if only wall-region behavior is pathological, prioritize wall treatment and near-wall mesh assumptions before broad residual tuning

likely_fixes:
- restore a single coherent turbulence field family instead of mixing k-epsilon and k-omega logic
- replace copied wall/opening turbulence BCs with ones consistent with the chosen family and patch role
- provide bounded, physically plausible inlet/opening turbulence quantities instead of arbitrary placeholders
- if the geometry and mesh imply a different wall-treatment regime, switch to a more coherent family / wall-treatment pairing before tuning numerics

escalation_path:
- if turbulence fields are simply missing or turbulence mode is not intentionally selected, route back to `turbulence-field-startup-mismatch`
- if the turbulence field family is coherent but the case still diverges, branch into mesh-quality, outlet-backflow, or steady-state numerics diagnosis
- if the real problem is solver-family or buoyancy framing rather than turbulence closure, exit this branch early instead of overfitting turbulence fixes

source_refs:
- official-openfoam-user-guide-turbulence-properties
- official-openfoam-turbulence-model-overview
- official-cfd-direct-turbulence-wall-function-guidance
- community-simscale-docs-k-epsilon-guidance
- community-simscale-docs-k-omega-sst-guidance

confidence: medium
notes:
- This node is narrower than `turbulence-field-startup-mismatch`: it is for cases where the turbulence layer exists, but the family/patch semantics are wrong.
- Many of these failures are structurally valid at the dictionary level and therefore easy for agents to miss without patch-role review.
