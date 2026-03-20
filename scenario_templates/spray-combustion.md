# Spray Combustion

scenario_name: spray-combustion
parent_template: reacting-combustion-flow-generic
steady_or_transient_intent: transient first, especially across injection onset and early parcel-cloud formation
representative_problem_class: spray combustion where injector timing, parcel properties, and carrier-phase reacting structure dominate the first startup checks

typical_solver_choices:
- sprayFoam as the primary official spray-combustion anchor in this pass
- the generic reacting parent only when the case is clearly reacting but the parcel and injector branch is still uncertain

key_dictionaries:
- 0/U
- 0/p or branch pressure variable
- 0/T
- carrier-phase species or reacting fields required by the chosen branch
- constant/thermophysicalProperties
- parcel or injection dictionaries required by the spray branch
- constant/turbulenceProperties when turbulence is enabled
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- keep injector timing, parcel properties, and carrier-phase reference state explicit from the first run
- compare injection dictionaries against the nearest spray tutorial lineage before editing breakup or evaporation detail
- watch whether instability begins exactly at injection onset

turbulence_guidance:
- only widen turbulence review after parcel and carrier-phase structure are coherent
- if the first failure coincides with injection onset, treat parcel structure as the first branch

mesh_guidance:
- inspect injector-near and ignition-near regions for local weakness rather than trusting only a global mesh pass
- local weakness near the initial spray path can masquerade as whole-case reacting instability

stability_risks:
- injection dictionaries mismatched to the carrier-phase branch
- parcel temperature or diameter state inconsistent with the intended injector setup
- a generic reacting template reused without the spray-specific parcel layer
- hotspot cells near injection onset or early evaporation regions

debug_priority_order:
- verify parcel and injection structure
- verify carrier-phase thermo coherence
- review startup controls around injection onset
- inspect injector-region hotspots
- only then widen to generic reacting stiffness or mesh review

source_refs:
- official-openfoam-tutorial-spray-combustion-sprayfoam
- official-openfoam-sprayfoam-guide
- official-openfoam-thermophysical-properties
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution
- community-cfd-online-sprayfoam-startup-thread

common_failure_branches:
- spray-injection-evaporation-coupling-startup-fragility
- reacting-startup-coupling-too-stiff
- thermo-chemistry-package-inconsistency
- critical-region-local-mesh-hotspot
- mesh-quality-driven-instability

recommended_playbooks:
- divergence-recovery-v1
- first-pass-case-setup-checklist
- mesh-quality-repair-v1
