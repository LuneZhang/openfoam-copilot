# Nonpremixed Diffusion Flame

scenario_name: nonpremixed-diffusion-flame
parent_template: reacting-combustion-flow-generic
steady_or_transient_intent: usually transient or staged startup first, because separated fuel and oxidizer streams need a stable reacting baseline before aggressive tuning
representative_problem_class: nonpremixed or diffusion-flame combustion where separated reactant streams and species BC coherence define the first structural branch

typical_solver_choices:
- reactingFoam as the primary official nonpremixed and diffusion-flame anchor in this pass
- the generic reacting parent only when the case is reacting but the stream structure is still too uncertain to narrow safely

key_dictionaries:
- 0/U
- 0/p or branch pressure variable
- 0/T
- required fuel, oxidizer, and product species fields
- constant/thermophysicalProperties
- chemistry or reacting dictionaries required by the chosen branch
- constant/turbulenceProperties when turbulence is enabled
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- keep fuel and oxidizer stream definitions explicit rather than hiding them behind generic inlet wording
- compare species BCs and stream temperatures against the nearest reacting tutorial family before editing chemistry detail
- verify reverse-flow-capable patches have meaningful return-state treatment

turbulence_guidance:
- only widen turbulence review after the separated-stream structure is coherent
- if instability begins at inlets or recirculating outlets, treat the problem as stream framing first

mesh_guidance:
- inspect mixing and flame regions for local weakness rather than trusting only the global mesh summary
- local cells in the first mixing region can look like chemistry failure while actually being transport fragility

stability_risks:
- fuel and oxidizer species BC mismatch
- outlet or reverse-flow regions feeding undefined return-state composition
- thermo or chemistry dictionaries copied from a generic reacting case without separated-stream review
- early hotspot growth in the first mixing region

debug_priority_order:
- verify separated-stream species and temperature structure
- verify reverse-flow and outlet treatment
- verify thermo and chemistry package coherence
- inspect the first mixing-region hotspot
- only then widen into generic reacting stiffness review

source_refs:
- official-openfoam-tutorial-nonpremixed-diffusion-reactingfoam
- official-openfoam-reactingfoam-guide
- official-openfoam-thermophysical-properties
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution
- community-cfd-online-reactingfoam-diffusion-flame-thread

common_failure_branches:
- nonpremixed-mixture-fraction-or-stoichiometric-inlet-mismatch
- outlet-backflow-role-confusion
- thermo-chemistry-package-inconsistency
- reacting-startup-coupling-too-stiff
- critical-region-local-mesh-hotspot
- mesh-quality-driven-instability

recommended_playbooks:
- boundary-condition-design-v1
- first-pass-case-setup-checklist
- divergence-recovery-v1
- mesh-quality-repair-v1
