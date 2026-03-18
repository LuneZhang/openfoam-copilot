# Buoyant Natural Convection / Room-Scale Thermal Flow

scenario_name: buoyant-natural-convection-room-scale
steady_or_transient_intent: often transient or pseudo-transient even when the final engineering question feels steady
representative_problem_class: buoyancy-driven indoor / enclosure / heated-wall flow where temperature and gravity actively drive circulation

typical_solver_choices:
- buoyantBoussinesqPimpleFoam for incompressible buoyant flow with small density variation
- buoyantSimpleFoam for steady buoyant workflows when the case is structurally mature and genuinely near steady

key_dictionaries:
- 0/U
- 0/p_rgh
- 0/T
- 0/nut
- 0/k
- 0/epsilon or 0/omega when turbulence is enabled
- constant/g
- constant/transportProperties or thermo-linked property file required by the chosen solver family
- constant/turbulenceProperties
- system/controlDict
- system/fvSchemes
- system/fvSolution

initialization_guidance:
- decide early whether the case belongs to Boussinesq-style incompressible buoyancy or a fuller thermo-compressible branch
- treat gravity direction, thermal reference state, and pressure convention as first-class setup items
- initialize temperature and buoyancy-driving fields with physically plausible gradients; do not hide uncertainty with all-zero placeholders
- use small startup timesteps and strong observability because thermal startup can look stable until buoyancy accelerates the flow

turbulence_guidance:
- if turbulence is enabled, check that the near-wall treatment still matches the thermal boundary-layer resolution strategy
- keep turbulence modeling subordinate to the buoyancy framing; the wrong pressure convention is usually more dangerous than the wrong closure model

mesh_guidance:
- resolve heated walls, vents, and plume paths before worrying about aesthetic global uniformity
- watch non-orthogonality and skewness near thermal boundary layers and geometry corners
- confirm that patch names clearly separate adiabatic, fixed-temperature, heat-flux, inlet, and outlet behavior

stability_risks:
- confusing `p` and `p_rgh` conventions or omitting `g`
- inconsistent thermal and flow BC pairing on openings and heated walls
- timestep too large for the early buoyant acceleration phase
- treating a buoyant case as if it were just an incompressible airflow template with one extra `T` file

debug_priority_order:
- verify buoyancy branch selection and pressure-variable convention
- verify `T`, `p_rgh`, and `g` consistency before any solver tuning
- verify thermal and flow BC coupling on all openings and walls
- run `checkMesh`, especially around heated boundaries and recirculation-prone corners
- review timestep/Courant control and conservative startup numerics
- only then touch relaxation factors or model upgrades

source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog
- official-openfoam-user-guide-solver-selection
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution
- official-openfoam-user-guide-turbulence-properties

common_failure_branches:
- p-vs-p_rgh-confusion
- buoyant-pressure-anchor-reference-mismatch
- thermo-chemistry-package-inconsistency
- continuity-error-growth
- courant-driven-transient-instability
- mesh-quality-driven-instability

recommended_playbooks:
- first-pass-case-setup-checklist
- boundary-condition-design-v1
- divergence-recovery-v1
- residual-diagnosis-v1
