# Troubleshooting Node — fireFoam Ventilation, Radiation, or HRR Coupling Mismatch

id: firefoam-ventilation-radiation-or-hrr-coupling-mismatch
symptom: A buoyant compartment-fire case destabilizes because ventilation openings, radiation coupling, heat-release-rate framing, ambient return state, or modified-pressure treatment are structurally inconsistent before later fire-model tuning.

probable_causes:
- openings are treated as pure exhaust even though hot gases can recirculate or outside air can re-enter
- radiation or heat-release-rate coupling is activated with inconsistent structural assumptions for the current fire branch
- `p_rgh`, gravity, or ambient reference framing is inconsistent with the buoyant fire branch
- fire source and ventilation layout were copied from mismatched tutorial lineages
- generic reacting tuning is being attempted before the compartment structure is coherent

first_checks:
- confirm the case really belongs to a buoyant compartment-fire branch rather than a generic reacting or non-buoyant branch
- verify `p_rgh`, gravity, and ambient reference framing before changing wider numerics
- inspect opening patches for meaningful thermal and species return-state treatment
- inspect whether radiation and heat-release-rate controls are coherent with the chosen ventilation and plume framing
- compare fire source and ventilation layout against the nearest official fireFoam tutorial lineage

deeper_checks:
- inspect whether the first instability forms near openings, the plume launch region, or the ambient interface rather than across the whole room
- separate opening/reference-state mismatch from a deeper thermo package or local hotspot problem
- only after the compartment structure is coherent, compare startup controls against a conservative transient fire baseline

likely_fixes:
- rebuild ventilation opening, radiation, and ambient reference treatment from the nearest compartment-fire tutorial baseline
- correct modified-pressure and gravity framing before wider reacting retuning
- keep the branch transient and conservative until opening exchange behaves physically

escalation_path:
- if modified-pressure anchoring is the dominant defect, route to `buoyant-pressure-anchor-reference-mismatch`
- if the real issue is reverse-flow semantics at one patch, route to `outlet-backflow-role-confusion`
- if a local region is driving the failure, route to `critical-region-local-mesh-hotspot`

source_refs:
- official-openfoam-firefoam-guide
- official-openfoam-tutorial-buoyant-fire-compartment-firefoam
- official-openfoam-hydrostatic-pressure-effects
- official-openfoam-docs-inletOutlet-backflow
- community-cfd-online-firefoam-compartment-fire-thread

confidence: medium
notes:
- Use this node when the family is already narrow enough to call it a compartment-fire branch.
- This node is not a replacement for the broader buoyant pressure-anchor node; it exists because fireFoam ventilation, radiation, and HRR coupling add a distinct first-check order.
