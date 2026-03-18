# Troubleshooting Node — `p` vs `p_rgh` Confusion

id: p-vs-p_rgh-confusion
symptom: A buoyant or gravity-influenced case behaves unphysically, diverges early, or shows pressure setup that seems copied from an incompressible non-buoyant template.

probable_causes:
- wrong pressure variable convention for the selected solver family
- gravity enabled but pressure treatment not adjusted to the buoyant branch
- field files or BCs copied from a `p`-based case into a `p_rgh` workflow
- thermal/buoyancy fields set up inconsistently with pressure treatment

first_checks:
- confirm the solver family really expects `p` or `p_rgh`
- inspect the active pressure field file under `0/`
- confirm gravity setup exists and is consistent where buoyancy is intended
- review boundary conditions for pressure and velocity together rather than separately

deeper_checks:
- compare the case against the nearest official buoyant tutorial family
- inspect temperature and thermal BCs for consistency with buoyancy framing
- confirm that reference-pressure logic was not copied from the wrong branch

likely_fixes:
- replace the wrong pressure-field convention with the solver-family-appropriate one
- rebuild pressure/velocity BCs as a coupled set for the buoyant branch
- align thermal and buoyancy fields with the chosen pressure formulation

escalation_path:
- if instability remains after pressure convention is fixed, branch into thermal-BC mismatch, timestep/startup sensitivity, or mesh-quality-driven instability

source_refs:
- official-openfoam-user-guide-solver-selection
- official-openfoam-thermophysical-properties
- official-openfoam-user-guide-controlDict

confidence: high
notes:
- This is a structural setup error class before it is a numerics problem.
