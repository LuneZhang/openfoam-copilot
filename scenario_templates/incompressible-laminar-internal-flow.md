# Incompressible Laminar Internal Flow

scenario_name: incompressible-laminar-internal-flow
steady_or_transient_intent: either; start from the nearest official laminar tutorial pattern
representative_problem_class: single-phase incompressible duct / channel / pipe flow at modest Reynolds number

typical_solver_choices:
- icoFoam for transient teaching-scale startup
- simpleFoam for steady internal-flow convergence once the case framing is correct

key_dictionaries:
- 0/U
- 0/p
- constant/transportProperties
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- start from physically plausible velocity and pressure scales rather than arbitrary zeros everywhere
- keep inlet velocity, outlet pressure, and wall no-slip roles explicit and complementary
- validate dimensions and units in `transportProperties` before touching numerics
- for a brand-new case, prefer serial-first validation with a short run window and dense writes

turbulence_guidance:
- keep turbulence disabled unless Reynolds number and modeling intent clearly require it
- do not carry over `k`, `epsilon`, or `omega` fields from a turbulent tutorial into a laminar template

mesh_guidance:
- begin with a simple, well-graded mesh and confirm patch naming before solver runs
- use `checkMesh` early; for this template, mesh confusion is usually a setup mistake rather than an advanced numerics problem
- keep aspect-ratio and non-orthogonality issues small enough that the case does not need heroic numerics

stability_risks:
- incompatible inlet/outlet pressure-velocity pairing
- viscosity copied from the wrong working fluid
- choosing a steady solver before the case structure and BCs are coherent
- overcomplicating numerics for a geometry that should converge with conservative defaults

debug_priority_order:
- confirm solver family and laminar intent
- confirm `U`/`p` fields and patch names match the mesh
- confirm `transportProperties` dimensions and magnitude
- run `checkMesh`
- review `fvSchemes` and `fvSolution` only after structure and BCs pass
- only then adjust timestep or relaxation behavior

source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-case-structure
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution
- official-openfoam-user-guide-transport-properties

common_failure_branches:
- patch-name-boundary-mismatch
- residual-plateau-fake-convergence
- continuity-error-growth
- mesh-quality-driven-instability
- wrong-solver-family-selection

recommended_playbooks:
- first-pass-case-setup-checklist
- residual-diagnosis-v1
- boundary-condition-design-v1
