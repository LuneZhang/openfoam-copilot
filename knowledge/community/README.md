# Community Knowledge

Store curated troubleshooting notes from high-value community sources here.

Only keep notes that add practical debugging or setup value beyond official docs.
Each note must be traceable to at least one recorded source entry.

Current Phase 1 focus:
- source triage framework
- troubleshooting source buckets
- first batch of high-value community source records under `source-records/`
- first troubleshooting nodes linked from those records
- Phase 2 expansion of boundary-condition / structural-failure evidence clusters (patch typing, pseudo-2D `empty` misuse, mesh-to-field consistency)
- Phase 2 expansion of outlet backflow / inlet-outlet role evidence so agents treat reverse-flow-at-outlet as a BC-structure clue instead of immediately blaming numerics
- Phase 2 expansion of buoyant pressure-anchor / reference-height evidence so agents distinguish wrong modified-pressure anchoring from generic continuity or `p`/`p_rgh` confusion
- Phase 2 expansion of turbulence family / wall-patch role evidence so agents distinguish missing turbulence fields from wrong turbulence-family semantics on walls and openings
- Phase 2 expansion of local mesh-hotspot evidence so agents distinguish globally passable meshes from locally poisonous bad-cell pockets in critical regions
- Phase 2 expansion of processor-count-sensitive parallel evidence so agents distinguish generic parallel-only failure from decomposition layouts that become pathological only after scaling rank count
- Phase 2 expansion of processor-boundary inconsistency evidence so agents prioritize processor-local diagnostics before trusting reconstructed global fields
- Phase 2 expansion of decomposition-fragmented-hotspot vs interface-semantic discrimination so agents can tell whether parallelization created the failure class or merely exposed a structural defect sooner
- Phase 2 expansion of divergence-localization evidence so agents inspect the first unstable region before broad numerics tuning
- Phase 2 expansion of continuity / pressure-anchoring evidence so agents check BC balance and fixed-pressure references before global numerics retuning
