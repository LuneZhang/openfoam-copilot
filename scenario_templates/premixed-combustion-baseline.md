# Premixed Combustion Baseline

scenario_name: premixed-combustion-baseline
parent_template: reacting-combustion-flow-generic
steady_or_transient_intent: usually transient or cautiously staged startup first, because ignition and premixed progress-variable structure are often too stiff for an aggressive first launch
representative_problem_class: premixed combustion where reactants enter as a mixed stream and the main startup branch is whether a XiFoam-style premixed structure is coherent

typical_solver_choices:
- XiFoam as the primary official premixed-combustion anchor in this pass
- the generic reacting parent only when the case is clearly reacting but not yet narrow enough for a premixed branch decision

key_dictionaries:
- 0/U
- 0/p or branch pressure variable
- 0/T
- premixed progress-variable or burned-fraction fields required by the chosen branch
- flame-wrinkling fields required by the chosen branch
- constant/thermophysicalProperties
- combustion-model dictionary required by the chosen branch
- constant/turbulenceProperties when turbulence is enabled
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- compare the case against the nearest premixed XiFoam tutorial lineage before improvising field names or model switches
- keep ignition and progress-variable structure explicit from the first run
- use conservative startup controls until the premixed flame structure behaves coherently

turbulence_guidance:
- keep turbulence as a secondary review until the premixed branch itself is coherent
- do not blame turbulence first when premixed ignition and progress fields are still uncertain

mesh_guidance:
- inspect flameholding and high-gradient premixed regions rather than trusting only the global mesh summary
- treat local weakness near the ignition or flame-front region as a likely startup amplifier

stability_risks:
- missing or mismatched premixed progress-variable fields
- ignition region defined loosely enough that the branch starts from an impossible premixed state
- nonpremixed or generic reacting structure copied into a premixed case
- local hotspot cells hidden near the initial flame region

debug_priority_order:
- verify the premixed branch and required field set
- verify ignition and progress-variable initialization
- verify thermo and BC coherence as one coupled premixed system
- inspect local hotspot regions near the flame anchor
- only then widen into generic reacting startup stiffness

source_refs:
- official-openfoam-tutorial-premixed-combustion-xifoam
- official-openfoam-xifoam-guide
- official-openfoam-thermophysical-properties
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

common_failure_branches:
- premixed-ignition-or-flame-speed-model-mismatch
- reacting-startup-coupling-too-stiff
- thermo-chemistry-package-inconsistency
- critical-region-local-mesh-hotspot
- mesh-quality-driven-instability

recommended_playbooks:
- first-pass-case-setup-checklist
- divergence-recovery-v1
- mesh-quality-repair-v1
- boundary-condition-design-v1
