# Troubleshooting Node — Critical-Region Local Mesh Hotspot

id: critical-region-local-mesh-hotspot
symptom: Global `checkMesh` output looks acceptable or only mildly warning-heavy, but the run still diverges or destabilizes from one localized region where a small cluster of bad cells appears to dominate the solution behavior.

probable_causes:
- a limited set of highly non-orthogonal or skewed cells sits inside a pressure-sensitive or high-gradient region
- near-wall layers, small geometric gaps, sharp corners, or outlet/interface neighborhoods contain locally dangerous cells hidden by acceptable global statistics
- the mesh is globally usable but locally too weak for the actual startup gradient field
- pressure-correction fragility is being triggered by a concentrated bad-cell pocket rather than by the average mesh state

first_checks:
- do not stop at the global `checkMesh` summary; locate where the worst cells actually are
- compare the first divergence hotspot with local non-orthogonality, skewness, and near-wall / interface cell quality
- ask whether the problematic cells sit in a region where pressure correction, recirculation, thermal plumes, or interfaces make the discretization unusually sensitive
- distinguish a few critical bad cells from a uniformly mediocre mesh, because the repair path differs
- inspect whether the same region also aligns with a CAD artifact, small gap, or layer collapse

deeper_checks:
- test whether the case only survives when numerics are made much more conservative, which often signals a locally fragile mesh rather than a purely global setup error
- inspect whether pressure-related equations are the first to show distress, which strengthens the local non-orthogonality hypothesis
- separate a local mesh hotspot from BC mistakes that merely happen to sit on the same patch
- if the hotspot is near an opening or interface, check whether BC structure and local mesh defects are reinforcing each other

likely_fixes:
- locally repair or remesh the hotspot region instead of assuming the whole mesh must be rebuilt
- simplify or suppress tiny CAD features that generate locally pathological cells
- improve near-wall or local transition meshing where the bad-cell pocket forms
- use conservative numerics only as a temporary validation aid while confirming that local mesh improvement actually removes the hotspot-driven failure

escalation_path:
- if the worst cells do not correlate with the failure region, route back to BC / solver-family / localized-divergence diagnosis instead of over-blaming the mesh
- if the whole mesh is broadly poor rather than locally pathological, route to `mesh-quality-driven-instability`
- if no local hotspot can be isolated, fall back to `localized-divergence-hotspot-triage` for wider symptom classification

source_refs:
- official-openfoam-user-guide-checkMesh
- official-openfoam-mesh-quality-guidance
- community-simscale-docs-mesh-quality-visualization
- community-simscale-docs-non-orthogonal-correctors
- community-simscale-kb-divergence-localization

confidence: medium
notes:
- This node is for “global mesh looks passable, local mesh is the real problem.”
- It exists to stop agents from being misled by acceptable average statistics when only a small critical region is numerically poisonous.
