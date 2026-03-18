# Residual Diagnosis v1

## Goal
Provide a practical interpretation framework for residual behavior in OpenFOAM so agents do not confuse every residual issue with the same root cause.

## Core principle
Residuals are diagnostics, not a universal truth metric. A case with poor residual behavior may reflect:
- structural setup errors
- boundary-condition inconsistency
- mesh-quality stress
- numerics that are too aggressive
- timestep/startup issues
- genuine physical unsteadiness

Therefore, residuals should be interpreted in context.

## First classification
When reviewing residuals, first ask:
1. Is the case intended to be steady or transient?
2. Which fields are misbehaving: pressure, velocity, turbulence, energy, species?
3. Is the issue monotonic blow-up, oscillation, plateau, or delayed instability?
4. Did the behavior start immediately or only after some evolution?

## Residual patterns and likely meanings

### Pattern A — Immediate blow-up
Typical meaning:
- strong setup inconsistency
- severe BC error
- bad mesh
- grossly unstable numerics

Priority checks:
1. case structure and required fields
2. BC consistency
3. checkMesh
4. numerics conservativeness

### Pattern B — Oscillatory residuals with no net improvement
Typical meaning:
- coupling instability
- aggressive convection/discretization
- insufficient relaxation
- poor mesh in critical regions

Priority checks:
1. `fvSchemes` and `fvSolution` together
2. SIMPLE/PISO/PIMPLE consistency
3. relaxation and linear-solver settings
4. mesh quality hot spots

### Pattern C — Residual plateau
Typical meaning:
- solver is stable but not making useful progress
- tolerances / relative tolerances may be hiding weak convergence
- setup may be physically inconsistent but not explosively unstable

Priority checks:
1. field-specific solver settings
2. whether stopping criteria are meaningful
3. whether the solution is physically acceptable, not just numerically quiet

### Pattern D — Delayed blow-up
Typical meaning:
- startup is initially survivable, but timestep / Courant / evolving gradients push the case unstable later
- can also indicate poor restart state or weak local mesh under evolving physics

Priority checks:
1. `deltaT`, `adjustTimeStep`, `maxCo`
2. monitor where instability appears first
3. inspect whether the issue starts after topology/flow-feature evolution

### Pattern E — Only one field misbehaves
Typical meaning:
- field-specific BC issue
- field-specific solver settings issue
- turbulence or thermo package mismatch

Priority checks:
1. the field’s BCs
2. the field’s solver settings in `fvSolution`
3. the field’s coupling assumptions in the chosen model family

## Important cautions

### Steady vs transient
- In steady cases, residuals often serve as a primary convergence indicator.
- In transient cases, residuals are important, but physical evolution means they should not be interpreted the same way as steady-run residuals.

### Pressure residuals are not the whole story
A case can show acceptable pressure residual behavior yet still be physically bad. Conversely, one noisy field does not automatically invalidate the whole run if the workflow is transient and physically justified.

## Practical diagnosis checklist
1. Identify the pattern type above.
2. Decide whether the issue is global or field-specific.
3. Check whether the case is structurally correct before tuning numerics.
4. Review mesh quality if residual behavior is unstable or highly sensitive.
5. Use residual behavior to prioritize next checks, not to skip setup review.

## Recommendation
- Never treat residuals in isolation from case intent.
- Classify the residual pattern before proposing fixes.
- Use residuals to choose the debugging branch: structure, BC, mesh, numerics, or runtime control.

## Output behavior for agents
When reporting residual issues, the agent should summarize:
1. residual pattern type
2. likely error class
3. top three checks in order
4. whether the issue looks structural, numerical, or runtime-driven

## Recommended Scenario Families

- `incompressible-laminar-internal-flow`
- `incompressible-rans-external-aerodynamics`
- `compressible-thermo-flow-generic`
- `multiphase-interface-flow-generic`
- `reacting-combustion-flow-generic`

## Primary Troubleshooting Node Handoffs

- `residual-plateau-fake-convergence`
- `continuity-error-growth`
- `steady-state-divergence-overaggressive-numerics`
- `courant-driven-transient-instability`
- `compressible-steady-startup-too-brittle`
- `multiphase-interface-initialization-mismatch`
- `reacting-startup-coupling-too-stiff`
