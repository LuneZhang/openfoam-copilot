# Troubleshooting Node — Decomposition-Fragmented Hotspot vs Interface Semantic Defect

id: decomposition-fragmented-hotspot-vs-interface-semantic-defect
symptom: A parallel failure localizes near an interface, opening, or coupled region, but it is unclear whether decomposition merely fragmented an already fragile local hotspot or whether the interface / boundary semantics are structurally wrong even before parallelization.

probable_causes:
- decomposition split a numerically fragile local hotspot into processor-local pieces that became less robust in parallel
- the interface or boundary-condition semantics are structurally wrong, and parallel execution simply exposes the defect sooner or more clearly
- both effects are present: a weak local region already exists, and decomposition amplifies it by worsening processor-local representation
- the first visible failure occurs near an interface, but the root cause may lie in local mesh / gradient concentration rather than in interface semantics themselves
- the interface looks suspicious only because processor-local evidence highlights the place where the global instability first becomes obvious

first_checks:
- ask whether the same physical region already looked weak in serial or low-rank runs, even if it did not fully fail there
- compare whether the failure follows processor-boundary placement changes or stays tied to the same physical interface/patch regardless of decomposition layout
- inspect whether the suspect region also contains a known local mesh hotspot, recirculation hotspot, or steep gradient zone
- verify the interface / opening / boundary semantics against the nearest correct tutorial family before assuming decomposition is the primary cause
- inspect processor-local logs to determine whether the first bad evidence is geometric/topological fragmentation or a semantic BC/interface inconsistency

deeper_checks:
- if changing processor count or decomposition method moves the failing region materially, favor the fragmentation/hotspot branch
- if the failure stays tied to the same physical patch with similar semantic symptoms across serial and parallel, favor the interface-semantic branch
- compare reconstructed global fields with processor-local evidence to see whether the hotspot is physical-location-stable or decomposition-layout-stable
- separate true interface semantic defects from local mesh weakness that just happens to sit near the interface
- if reverse flow, pressure anchoring, or turbulence companion fields are suspect at the same location, route into the corresponding BC structural nodes instead of overfitting the parallel explanation

likely_fixes:
- if hotspot fragmentation dominates, use a safer decomposition, preserve the sensitive region better, or improve the local mesh / startup strategy
- if interface semantics dominate, repair BC roles, interface setup, pressure treatment, or companion fields before further parallel tuning
- if both are interacting, first fix the structural semantic defect, then retest with a decomposition that is less pathological around the sensitive region
- use processor-local diagnostics to decide whether decomposition is the amplifier or the root cause

escalation_path:
- if the evidence is mainly rank-threshold-sensitive and moves with decomposition layout, route to `processor-count-sensitive-parallel-failure`
- if the evidence is mainly processor-boundary-local and reconstruction hides it, keep `processor-boundary-field-inconsistency` active as the parent branch
- if the real issue is local mesh weakness, route to `critical-region-local-mesh-hotspot`
- if the real issue is boundary / interface semantics, route to the narrower BC structural node instead of staying inside the parallel branch

source_refs:
- official-openfoam-user-guide-parallel
- official-openfoam-decomposePar-guide
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-user-guide-checkMesh
- community-openfoam-bugtracker-coupled-patch-parallel-crash
- community-openfoam-bugtracker-cyclicami-single-sided-parallel-crash
- community-simscale-kb-divergence-localization

confidence: medium
notes:
- This node is a discriminator node: its job is to tell agents whether parallelization created the failure class or merely revealed a pre-existing structural defect sooner.
- Many expensive debugging loops happen because these two branches are mixed together.
