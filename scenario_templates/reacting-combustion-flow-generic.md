# Reacting / Combustion Flow — Generic Template

scenario_name: reacting-combustion-flow-generic
scenario_role: active parent and fallback for combustion cases when no narrow family is clearly dominant
narrow_specializations:
- premixed-combustion-baseline
- nonpremixed-diffusion-flame
- buoyant-fire-compartment
- partially-premixed-recirculating-combustor
- spray-combustion
steady_or_transient_intent: usually transient or cautiously staged startup first, because thermo, chemistry, and flow coupling are often too stiff for an immediate aggressive solve
representative_problem_class: reacting or combustion flow where thermo, species, and heat-release coupling materially affect the solution behavior

typical_solver_choices:
- reactingFoam-family workflow for transient reacting/compressible combustion-style startup when thermo and chemistry are strongly coupled
- other reacting-family solvers only after confirming the chemistry model class, thermo package, and flow regime really match the target problem

key_dictionaries:
- 0/U
- 0/p or solver-family pressure variable
- 0/T or solver-family thermal field
- 0/ species fields required by the selected reacting branch
- 0/nut
- 0/k
- 0/epsilon or 0/omega when turbulence is enabled
- constant/thermophysicalProperties
- constant/chemistryProperties or solver-family chemistry dictionaries
- constant/turbulenceProperties when turbulence is enabled
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- begin from the nearest official reacting or combustion tutorial family rather than extending a non-reacting template ad hoc
- if one of the five narrow combustion families clearly matches the case, route there first and keep this template as the fallback parent rather than the primary working surface
- make thermo package, chemistry model class, and species-field set explicit at startup
- initialize pressure, temperature, and species fields on physically plausible scales; do not treat chemistry fields as optional decorations
- when structure is still uncertain, prefer a conservative staged or transient startup before pushing an aggressive target solve
- keep startup controls conservative until thermo and species evolution behave coherently

turbulence_guidance:
- only add turbulence complexity after thermo and chemistry structure are coherent
- turbulence/combustion coupling should be reviewed as part of solver-family fit, not as an isolated late tweak

mesh_guidance:
- inspect regions with expected flame fronts, strong heat release, recirculation, injection, or steep scalar gradients
- do not stop at global mesh acceptability; look for critical local regions where reacting source terms and thermal gradients will be numerically fragile
- poor local mesh quality in high-gradient reacting regions often looks like chemistry failure while actually being a mesh/transport fragility problem

stability_risks:
- thermo package inconsistent with reacting solver family
- chemistry model class or species set inconsistent with the intended physical problem
- using non-reacting or weakly coupled setup intuition for a tightly coupled reacting case
- aggressive startup numerics before thermo/species fields form a stable coupled baseline
- local hotspot regions where mesh, transport, and source terms interact pathologically

debug_priority_order:
- verify reacting solver family and required field/dictionary set
- verify thermo package and chemistry model coherence
- verify thermal, species, and pressure-related BCs as a coupled reacting system
- run `checkMesh` with flame-front / scalar-gradient / hotspot regions in mind
- review conservative startup timestep and numerics before touching model-detail tuning
- only then escalate into turbulence/chemistry-detail refinement

source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-solver-selection
- official-openfoam-thermophysical-properties
- official-openfoam-compressible-setup-guidance
- official-openfoam-user-guide-controlDict
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
- mesh-quality-repair-v1
- residual-diagnosis-v1
