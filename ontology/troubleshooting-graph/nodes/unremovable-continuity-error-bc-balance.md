# Troubleshooting Node — Unremovable Continuity Error from BC Balance / Pressure Anchoring

id: unremovable-continuity-error-bc-balance
symptom: The solver stops with a continuity error that cannot be removed, or continuity residuals remain dominated by global mass-balance inconsistency instead of converging downward.

probable_causes:
- inlet and outlet velocity / pressure boundary conditions are not mutually consistent
- no effective fixed-pressure anchor exists, leaving pressure level underconstrained for the chosen setup
- custom boundary conditions invert `fixedValue` / `zeroGradient` roles between velocity and pressure
- a nominally open-flow setup is actually configured more like a closed domain without proper reference-pressure treatment

first_checks:
- inspect inlet and outlet pressure/velocity boundary conditions as a coupled pair rather than field by field
- verify whether the case has at least one meaningful fixed-pressure anchor or equivalent reference-pressure treatment
- compare the BC combination against the nearest official tutorial for the same solver family and topology
- confirm whether the issue is a true BC-balance problem or a buoyant / compressible `p` vs `p_rgh` framing error

deeper_checks:
- if the domain is effectively closed, check whether pressure reference is being provided through the solver controls instead of a patch BC
- inspect whether the target quantity is mass-flow, volumetric-flow, or pressure-driven, and whether the BC pair matches that intention
- review whether continuity error appears immediately at startup (structural BC issue) or only after numerics degrade later (secondary symptom)
- if continuity failure coexists with buoyancy or thermal coupling, branch into `p-vs-p_rgh-confusion` instead of forcing generic outlet-pressure advice

likely_fixes:
- correct inlet/outlet BC pairing so velocity and pressure constraints are complementary rather than contradictory
- add or repair a fixed-pressure anchor / valid reference-pressure treatment for the topology
- replace ad hoc custom BC combinations with a known-good official tutorial pattern for the same solver family
- only after BC/reference consistency is restored, retune timestep, relaxation, or discretization if instability remains

escalation_path:
- if pressure variable choice itself is wrong for the solver family, route to `p-vs-p_rgh-confusion`
- if BCs are structurally consistent but continuity still grows later in the run, route to `continuity-error-growth`
- if the issue localizes to one outlet patch or geometry defect, route into mesh / patch-specific nodes rather than repeating global numerics changes

source_refs:
- community-simscale-kb-continuity-error
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-user-guide-fvSolution
- official-openfoam-user-guide-controlDict

confidence: medium
notes:
- Treat this node as a pressure-anchoring / BC-consistency branch, especially for open-domain setups that fail before any meaningful physical evolution occurs.
