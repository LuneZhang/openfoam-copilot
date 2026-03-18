# Troubleshooting Node — Continuity Error Growth

id: continuity-error-growth
symptom: Continuity errors grow steadily or remain unacceptably large, often alongside unstable pressure-velocity behavior.

probable_causes:
- pressure-velocity coupling not stabilizing cleanly
- timestep or Courant control too loose for the case
- poor mesh quality amplifying pressure correction difficulty
- boundary conditions causing global mass-balance inconsistency
- solver family or pressure treatment mismatch in buoyant/compressible branches

first_checks:
- inspect continuity error trend together with pressure residual behavior
- review pressure/velocity boundary conditions as a coupled set
- verify timestep / `adjustTimeStep` / `maxCo` logic
- run `checkMesh` and classify whether mesh quality could be stressing pressure correction

deeper_checks:
- verify SIMPLE/PISO/PIMPLE settings match the chosen application
- compare against the nearest official tutorial family for pressure treatment and runtime controls
- inspect whether the problem appears only in parallel or already in serial

likely_fixes:
- reduce timestep or tighten Courant control
- correct pressure/velocity BC inconsistencies
- use more conservative startup numerics for pressure-velocity coupling
- resolve mesh issues before repeatedly changing relaxation alone

escalation_path:
- if continuity errors persist after these checks, branch into p-vs-p_rgh-confusion, mesh-quality-driven-instability, or parallel-only-failure

source_refs:
- official-openfoam-user-guide-fvSolution
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-checkMesh

confidence: high
notes:
- Continuity error growth is usually a symptom bucket, not a single root cause.
