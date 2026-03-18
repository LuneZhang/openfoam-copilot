# Compressible Thermo Flow — Generic Template

scenario_name: compressible-thermo-flow-generic
steady_or_transient_intent: either, but transient or pseudo-transient startup is often safer when thermal/compressibility coupling is strong
representative_problem_class: compressible single-phase flow with important density and energy coupling

typical_solver_choices:
- rhoPimpleFoam for transient compressible flow with strong coupling or startup sensitivity
- rhoSimpleFoam for steady compressible workflows once structure and thermo setup are already coherent

key_dictionaries:
- 0/U
- 0/p
- 0/T or solver-family thermal fields
- 0/nut
- 0/k
- 0/epsilon or 0/omega when turbulence is enabled
- constant/thermophysicalProperties
- constant/turbulenceProperties when turbulence is enabled
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- begin from a compressible tutorial family rather than extending an incompressible template ad hoc
- state clearly whether temperature, density, and energy coupling are central to the case
- initialize pressure, temperature, and velocity on physically plausible scales; avoid arbitrary zero-filled startup fields
- when structure is still uncertain, prefer transient or pseudo-transient startup over immediately forcing a brittle steady compressible solve
- use conservative startup controls when thermo and momentum are tightly coupled

turbulence_guidance:
- if turbulence is enabled, ensure the turbulence field set and wall treatment strategy match the chosen compressible workflow
- do not blame turbulence first when thermo package or pressure setup is still unverified

mesh_guidance:
- checkMesh early with attention to regions where shocks, strong gradients, thermal fronts, or narrow openings may develop
- do not stop at global mesh pass/fail; inspect whether one critical region is numerically much weaker than the average mesh summary suggests
- poor cells in high-gradient compressible regions often produce instability that looks like solver weakness
- if the mesh is only marginally acceptable, prefer conservative numerics and smaller timesteps at startup

stability_risks:
- thermophysical package inconsistent with solver family
- using incompressible mental models for pressure/temperature coupling
- thermal and pressure BCs that are syntactically valid but physically mismatched for the intended compressible branch
- aggressive startup numerics in a tightly coupled compressible run
- inadequate initialization of temperature or pressure scale
- local mesh weakness hidden inside a globally passable mesh summary

debug_priority_order:
- verify solver family and compressible intent
- verify `thermophysicalProperties` coherence
- verify thermal and pressure-related BC consistency
- run `checkMesh` and look for critical local hotspots, not only global acceptability
- review conservative startup numerics and timestep strategy, especially whether a transient/pseudo-transient path is safer than an immediate steady solve
- only then refine turbulence or solver controls

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
- patch-name-boundary-mismatch
- mesh-quality-driven-instability
- critical-region-local-mesh-hotspot
- courant-driven-transient-instability
- steady-state-divergence-overaggressive-numerics
- compressible-steady-startup-too-brittle

recommended_playbooks:
- first-pass-case-setup-checklist
- boundary-condition-design-v1
- divergence-recovery-v1
- mesh-quality-repair-v1
- residual-diagnosis-v1
