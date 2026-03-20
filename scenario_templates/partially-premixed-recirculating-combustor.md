# Partially Premixed Recirculating Combustor

scenario_name: partially-premixed-recirculating-combustor
parent_template: reacting-combustion-flow-generic
steady_or_transient_intent: usually transient or staged startup first, because recirculation-zone formation and pilot stabilization matter before any aggressive target solve
representative_problem_class: partially premixed combustor where a premixed flame branch exists but the first structural risk is recirculating return-state and pilot-stream coherence

typical_solver_choices:
- XiFoam as the primary official premixed anchor in this pass when the combustor still behaves like a premixed progress-variable branch
- other reacting branches only after confirming the pilot, return-state, and recirculation structure do not fit the premixed anchor

key_dictionaries:
- 0/U
- 0/p or branch pressure variable
- 0/T
- premixed progress-variable or related premixed fields required by the chosen branch
- any extra pilot or secondary-stream species fields required by the chosen branch
- constant/thermophysicalProperties
- combustion-model dictionary required by the chosen branch
- constant/turbulenceProperties when turbulence is enabled
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- define pilot, main-stream, and recirculating return state explicitly
- treat reverse-flow-capable outlets as part of the combustor setup, not as generic exhaust
- compare flameholder or recirculation-region structure against the nearest premixed tutorial lineage before widening the model family

turbulence_guidance:
- keep turbulence review secondary until the return-state and pilot structure is coherent
- if the run destabilizes near reverse-flow regions, treat that as a branch-selection clue before later model tuning

mesh_guidance:
- inspect flameholder, recirculation bubble, and pilot regions for local weakness rather than trusting the domain-average mesh summary
- local weakness in the recirculating hotspot can masquerade as a global reacting failure

stability_risks:
- returning mixed products are left undefined at reverse-flow patches
- a plain premixed template is reused without recirculation-specific state definition
- pilot and main streams are structurally inconsistent
- hotspot cells live near the flameholder or return path

debug_priority_order:
- verify return-state and reverse-flow treatment
- verify pilot and main-stream coherence
- verify premixed branch structure
- inspect flameholder and recirculation hotspots
- only then widen into generic reacting stiffness review

source_refs:
- official-openfoam-tutorial-premixed-combustion-xifoam
- official-openfoam-xifoam-guide
- official-openfoam-docs-inletOutlet-backflow
- official-openfoam-thermophysical-properties
- community-simscale-docs-pressure-outlet-backflow

common_failure_branches:
- recirculating-combustor-flame-holding-or-backflow-mismatch
- outlet-backflow-role-confusion
- premixed-ignition-or-flame-speed-model-mismatch
- reacting-startup-coupling-too-stiff
- critical-region-local-mesh-hotspot
- mesh-quality-driven-instability

recommended_playbooks:
- boundary-condition-design-v1
- first-pass-case-setup-checklist
- divergence-recovery-v1
- mesh-quality-repair-v1
