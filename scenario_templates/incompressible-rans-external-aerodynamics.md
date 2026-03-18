# Incompressible RANS External Aerodynamics

scenario_name: incompressible-rans-external-aerodynamics
steady_or_transient_intent: usually steady first-pass RANS, with transient escalation when separation or unsteadiness dominates
representative_problem_class: external flow around bluff bodies or airfoils where turbulence closure is required

typical_solver_choices:
- simpleFoam for steady incompressible RANS startup
- pimpleFoam when transient behavior or startup instability makes a steady-only view misleading

key_dictionaries:
- 0/U
- 0/p
- 0/nut
- 0/k
- 0/epsilon or 0/omega
- constant/transportProperties
- constant/turbulenceProperties
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- start from the closest official turbulent external-flow tutorial instead of cloning a laminar case and adding turbulence later
- make freestream direction, reference velocity scale, and outlet pressure convention explicit
- initialize turbulence quantities from a bounded estimate tied to inlet turbulence assumptions, not arbitrary near-zero guesses
- plan runtime observability from the start with residuals and force/monitor outputs

turbulence_guidance:
- choose one turbulence family intentionally and ensure the matching fields exist
- verify wall treatment and near-wall mesh assumptions before blaming numerics
- do not mix `k-epsilon` and `k-omega` style field sets or wall functions accidentally

mesh_guidance:
- check external-domain size, wake resolution, and boundary-layer treatment before tuning relaxation factors
- inspect wall-region mesh quality because poor near-wall cells often masquerade as turbulence-model instability
- keep serial-first checks if the case size permits; parallel adds another failure surface too early

stability_risks:
- missing or inconsistent turbulence fields and wall functions
- wake/outlet reflections caused by a too-small external domain
- aggressive convection schemes before the case reaches a stable startup state
- pressure level confusion when comparing incompressible gauge-pressure outputs to physical expectations

debug_priority_order:
- verify solver family, steady/transient intent, and turbulence model choice
- verify required turbulence fields and wall treatment consistency
- verify external-domain BC logic for inlet, outlet, symmetry/far-field, and wall patches
- run `checkMesh` with attention to near-wall and wake-critical regions
- review conservative startup numerics and relaxation strategy
- escalate to transient workflow only if the physics or residual behavior demands it

source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-solver-selection
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution
- official-openfoam-user-guide-turbulence-properties
- official-openfoam-function-objects

common_failure_branches:
- turbulence-field-startup-mismatch
- turbulence-field-family-patch-role-mismatch
- steady-state-divergence-overaggressive-numerics
- mesh-quality-driven-instability
- patch-name-boundary-mismatch
- residual-plateau-fake-convergence
- wrong-solver-family-selection

recommended_playbooks:
- first-pass-case-setup-checklist
- boundary-condition-design-v1
- residual-diagnosis-v1
- mesh-quality-repair-v1
