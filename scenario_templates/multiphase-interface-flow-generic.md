# Multiphase Interface Flow — Generic Template

scenario_name: multiphase-interface-flow-generic
steady_or_transient_intent: usually transient first, because interface motion and phase interaction are inherently time dependent
representative_problem_class: free-surface or interface-resolving multiphase flow where multiple phase fields are central to the setup

typical_solver_choices:
- interFoam-family workflow for transient free-surface/interface-resolving startup
- other multiphase-family solvers only after confirming the physical model class truly matches the target problem

key_dictionaries:
- 0/U
- 0/p_rgh or pressure variable expected by the chosen multiphase branch
- 0/alpha.* or other required phase fields
- constant/g
- constant/transportProperties or phase-property dictionaries required by the selected branch
- constant/polyMesh
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- make the phase topology explicit at startup; the initial interface is part of the problem statement, not a minor detail
- use the nearest official multiphase tutorial family as the structural baseline
- initialize phase fractions, gravity direction, and pressure convention coherently
- do not borrow a single-phase setup and only graft `alpha.*` fields onto it; treat interface initialization as core structure
- keep startup timesteps conservative until the interface motion is demonstrably stable

turbulence_guidance:
- only add turbulence complexity after the multiphase structure itself is coherent
- in many unstable multiphase starts, phase setup and interface numerics are more urgent than turbulence-model sophistication

mesh_guidance:
- resolve interface-relevant regions and expected free-surface motion paths
- pay special attention to cell quality where interface curvature or phase exchange is important
- do not stop at global mesh acceptability; look for critical local regions where interface transport, curvature, or opening behavior will be numerically fragile
- poor mesh quality near the interface often amplifies unphysical smearing or instability

stability_risks:
- wrong phase-field initialization
- confusion between `p` and `p_rgh` style pressure treatment in gravity-coupled workflows
- timestep too large for interface transport
- borrowing a single-phase setup and then grafting multiphase fields onto it
- pressure / phase-field / opening BCs that are individually legal but structurally mismatched as a coupled interface system
- local mesh weakness hidden near the interface or opening region
- decomposition-sensitive interface fragmentation in parallel runs

debug_priority_order:
- verify multiphase solver family and required field set
- verify pressure convention and gravity setup
- verify phase-field initialization and BCs as a coupled interface system
- run `checkMesh` with interface-critical regions and local hotspots in mind
- review conservative startup timestep and numerics
- if serial is clean but parallel is not, route into parallel/interface diagnosis before broad numerics retuning
- only then escalate to model-detail tuning

source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-solver-selection
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

common_failure_branches:
- p-vs-p_rgh-confusion
- multiphase-interface-initialization-mismatch
- courant-driven-transient-instability
- mesh-quality-driven-instability
- critical-region-local-mesh-hotspot
- processor-boundary-field-inconsistency
- decomposition-fragmented-hotspot-vs-interface-semantic-defect
- wrong-solver-family-selection
- patch-name-boundary-mismatch

recommended_playbooks:
- first-pass-case-setup-checklist
- boundary-condition-design-v1
- divergence-recovery-v1
- mesh-quality-repair-v1
- residual-diagnosis-v1
