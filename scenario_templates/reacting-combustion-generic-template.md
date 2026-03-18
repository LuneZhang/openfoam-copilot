# Reacting / Combustion Flow — Generic Template (deprecated alias)

Deprecated note:
- canonical template: `reacting-combustion-flow-generic.md`
- keep this file only as a compatibility alias during the validation-stage cleanup

scenario_name: reacting-combustion-generic-template
steady_or_transient_intent: usually transient or staged startup, because chemistry, heat release, and turbulence coupling create strong instability risk
representative_problem_class: reacting flow where species transport, heat release, and thermo-chemistry coupling are central

typical_solver_choices:
- reacting/compressible combustion-family solver nearest to the official tutorial pattern for the intended chemistry model
- transient family first when startup robustness matters more than nominal steady-state convenience

key_dictionaries:
- 0/U
- 0/p or solver-family pressure variable
- 0/T and/or energy-related fields required by the selected branch
- species fields required by the chemistry setup
- turbulence fields when turbulence is enabled
- constant/thermophysicalProperties
- chemistry / reaction-property dictionaries required by the chosen branch
- constant/turbulenceProperties where applicable
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- start from the closest official reacting or combustion tutorial family, not from a generic compressible case with chemistry appended later
- make thermo, chemistry, and species assumptions explicit before runtime tuning
- initialize temperature, pressure, velocity, and species fields with physically plausible scales
- use conservative startup controls because heat release can destabilize a case after apparently normal first iterations

turbulence_guidance:
- if turbulence is enabled, verify that turbulence, mixing, and combustion assumptions are at least structurally compatible
- do not use turbulence tuning as a substitute for fixing chemistry/thermo inconsistency

mesh_guidance:
- ensure critical flame / reaction / mixing regions are not under-resolved by obviously poor-quality cells
- checkMesh is still mandatory; reacting cases often punish marginal mesh more harshly than simple flow cases
- prioritize quality in regions of strong scalar and temperature gradients

stability_risks:
- thermo/chemistry package inconsistency
- missing or inconsistent species fields
- unrealistic initial temperature/species state
- trying to force a nominally steady reacting workflow before the transient startup is under control

debug_priority_order:
- verify reacting/combustion solver family choice
- verify thermo and chemistry dictionary coherence
- verify species/thermal/pressure field presence and BC consistency
- run `checkMesh`
- review conservative startup timestep and numerics
- only then tune turbulence, chemistry detail, or relaxation strategy

source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-solver-selection
- official-openfoam-thermophysical-properties
- official-openfoam-compressible-setup-guidance
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

common_failure_branches:
- thermo-chemistry-package-inconsistency
- wrong-solver-family-selection
- reacting-startup-coupling-too-stiff
- courant-driven-transient-instability
- critical-region-local-mesh-hotspot
- mesh-quality-driven-instability
- turbulence-field-startup-mismatch
- patch-name-boundary-mismatch

recommended_playbooks:
- first-pass-case-setup-checklist
- boundary-condition-design-v1
- divergence-recovery-v1
- residual-diagnosis-v1
- mesh-quality-repair-v1
