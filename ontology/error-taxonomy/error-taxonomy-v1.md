# Error Taxonomy v1

## Purpose
Provide a first structured classification of common OpenFOAM setup and runtime failure types.
This taxonomy is designed for agent routing and troubleshooting prioritization.

## Class A — Structural setup errors
These are problems where the case is incomplete or internally inconsistent before numerics meaningfully matter.

Typical symptoms:
- missing dictionary/file errors
- unknown field / patch / keyword errors
- solver starts against the wrong field set

Typical roots:
- missing required fields under `0/`
- wrong case structure
- wrong solver family for the copied template
- wrong patch names or dictionary placement

Default first checks:
1. solver/application identity
2. case structure (`0/`, `constant/`, `system/`)
3. required fields and dictionary presence
4. mesh patch names vs boundaryField names

## Class B — Boundary-condition errors
These are cases where field constraints at patches are contradictory, incomplete, or physically unreasonable.

Typical symptoms:
- immediate divergence after startup
- unphysical recirculation or pressure behavior
- solver instability despite seemingly valid numerics

Typical roots:
- over-constrained or under-constrained coupled variables
- wrong pressure variable conventions (`p` vs `p_rgh`)
- turbulence-field BC mismatch
- thermal or buoyancy BC inconsistency

Default first checks:
1. review `U`/pressure complementarity
2. verify solver-family-specific pressure treatment
3. verify turbulence field BCs
4. verify patch type semantics (wall/inlet/outlet/symmetry/empty)

## Class C — Mesh-quality-driven instability
These are cases where discretization is being stressed by poor mesh quality.

Typical symptoms:
- floating point exception
- residual oscillation
- solver becomes unstable under aggressive schemes or timestep
- instability localized to sharp-gradient regions

Typical roots:
- high non-orthogonality
- high skewness
- poor local cells in critical regions
- invalid or near-invalid topology

Default first checks:
1. run `checkMesh`
2. classify fatal vs severe vs manageable warnings
3. inspect worst-cell locations
4. correlate unstable regions with poor cells

## Class D — Numerics aggressiveness / coupling instability
These are cases where the equations and mesh may be structurally valid, but the numerical setup is too ambitious.

Typical symptoms:
- residual blow-up
- oscillatory convergence
- nonphysical overshoot/undershoot
- sensitivity to startup conditions

Typical roots:
- aggressive convection schemes
- inadequate relaxation
- unsuitable solver tolerances
- mismatch between application and SIMPLE/PISO/PIMPLE block

Default first checks:
1. review `fvSchemes` and `fvSolution` together
2. confirm algorithm block matches solver family
3. reduce numerical aggressiveness
4. review relaxation and tolerances

## Class E — Initialization / timestep / runtime-control instability
These are cases where startup state or temporal controls push a valid case into unstable evolution.

Typical symptoms:
- divergence only after several steps
- Courant number growth
- run becomes unstable under larger `deltaT`
- adaptive timestep collapses to tiny values

Typical roots:
- poor initial fields
- overly large `deltaT`
- weak control of `maxCo`
- restart from unsuitable previous state

Default first checks:
1. inspect `controlDict`
2. review `deltaT`, `adjustTimeStep`, `maxCo`
3. compare startup fields to expected physical scale
4. test more conservative startup controls

## Class F — Physics/model mismatch
These are cases where the chosen solver/model family does not fit the actual problem.

Typical symptoms:
- repeated instability that survives numerics tuning
- wrong field expectations
- results structurally inconsistent with expected behavior

Typical roots:
- wrong solver family
- wrong turbulence model class
- wrong compressibility assumption
- wrong thermo package / multiphase framing

Default first checks:
1. restate the physics problem in one sentence
2. re-check solver family map
3. compare against nearest official tutorial family
4. verify required dictionaries and model fields

## Class G — Parallel workflow errors
These are failures introduced or made worse by decomposition and parallel execution.

Typical symptoms:
- run works poorly only in parallel
- decomposition/reconstruction issues
- processor-local instability or file inconsistency

Typical roots:
- bad decomposition setup
- mismatch between processor count and decomposition plan
- parallel execution started before serial sanity was established

Default first checks:
1. validate serial case first where practical
2. review `decomposeParDict`
3. inspect processor logs separately
4. separate decomposition issues from solver instability

## Routing rule for agents
When troubleshooting:
1. classify the problem into one or two classes above
2. run first checks in class order
3. only escalate to deeper tuning after structural classes are cleared

## Priority order heuristic
Default debugging order should usually be:
1. Structural setup
2. Boundary conditions
3. Mesh quality
4. Solver/model family fit
5. Numerics and relaxation
6. Initialization / timestep
7. Parallel-specific issues

This order is not absolute, but it is a strong default starting point.
