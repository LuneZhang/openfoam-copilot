# Troubleshooting Node — Wrong Solver Family Selection

id: wrong-solver-family-selection
symptom: The case repeatedly behaves incorrectly or unstably even after numerics are softened, because the selected solver family does not match the actual physics.

probable_causes:
- incompressible solver chosen for a problem with important density/thermal coupling
- steady workflow chosen for a case whose startup or physics is fundamentally transient
- single-phase framing used for a multiphase problem
- generic flow solver chosen where reacting, buoyant, or thermo-coupled treatment is essential

first_checks:
- restate the physics problem in one sentence
- classify the case by incompressible/compressible, steady/transient, single-phase/multiphase, buoyant/reacting axes
- compare the chosen solver against the nearest official tutorial family
- inspect whether the active field set and dictionaries actually match the intended physics branch

deeper_checks:
- review whether apparent BC or thermo errors are really downstream symptoms of the wrong solver family
- inspect whether the pressure variable convention fits the chosen branch
- inspect whether the case keeps inheriting templates from a visually similar but physically different problem class

likely_fixes:
- move to the correct solver family branch before further tuning
- rebuild required field/property dictionaries to match that branch
- restart from the nearest official tutorial structure instead of patching the wrong template indefinitely

escalation_path:
- once the solver family is corrected, re-check BCs, thermo/turbulence fields, and numerics conservativeness from scratch

source_refs:
- official-openfoam-user-guide-solver-selection
- official-openfoam-tutorial-catalog
- official-openfoam-tutorial-conventions

confidence: high
notes:
- Wrong solver family is a top-level setup error, not a late-stage tuning issue.
