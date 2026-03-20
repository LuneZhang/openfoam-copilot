# Buoyant Fire Compartment

scenario_name: buoyant-fire-compartment
parent_template: reacting-combustion-flow-generic
steady_or_transient_intent: transient first, because buoyancy, fire growth, and ventilation exchange are part of the physical startup path
representative_problem_class: buoyant compartment-fire combustion where `p_rgh`, openings, ambient return state, and fire-source framing dominate the first checks

typical_solver_choices:
- fireFoam as the primary official buoyant fire and compartment-fire anchor in this pass
- the generic reacting parent only when the case is clearly reacting but the fire and ventilation framing is still uncertain

key_dictionaries:
- 0/U
- 0/p_rgh
- 0/T
- species or fire fields required by the chosen branch
- constant/g
- constant/thermophysicalProperties
- fire or combustion-model dictionaries required by the chosen branch
- constant/radiationProperties when radiation is enabled
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- keep the ambient and opening return state explicit at startup
- verify modified-pressure framing before tuning ventilation numerics
- compare fire source and ventilation layout against the nearest compartment-fire tutorial lineage

turbulence_guidance:
- only widen turbulence review after the buoyancy and opening structure is coherent
- do not blame turbulence first when `p_rgh` and opening state are still uncertain

mesh_guidance:
- inspect plume, opening, and near-fire regions for local weakness rather than trusting a global pass result
- local weakness near the source or vent path can masquerade as whole-room reacting instability

stability_risks:
- wrong `p_rgh` or ambient reference framing
- openings treated as pure outflow when hot gases can re-enter
- fire source, buoyancy, and ambient state copied from mismatched tutorial branches
- local hotspot cells near plume launch or vent exchange paths

debug_priority_order:
- verify `p_rgh`, gravity, and ambient reference framing
- verify opening backflow and return-state treatment
- verify fire-source and thermo coherence
- inspect plume and opening hotspot regions
- only then widen into generic reacting instability review

source_refs:
- official-openfoam-tutorial-buoyant-fire-compartment-firefoam
- official-openfoam-firefoam-guide
- official-openfoam-hydrostatic-pressure-effects
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-user-guide-controlDict
- community-cfd-online-firefoam-compartment-fire-thread

common_failure_branches:
- firefoam-ventilation-radiation-or-hrr-coupling-mismatch
- buoyant-pressure-anchor-reference-mismatch
- outlet-backflow-role-confusion
- thermo-chemistry-package-inconsistency
- courant-driven-transient-instability
- critical-region-local-mesh-hotspot

recommended_playbooks:
- boundary-condition-design-v1
- first-pass-case-setup-checklist
- divergence-recovery-v1
- mesh-quality-repair-v1
