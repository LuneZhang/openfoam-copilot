# fvSchemes and fvSolution Basics

id: official-fvSchemes-fvSolution-basics
problem_class: numerics
confidence: high
source_refs:
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

## Why this note exists

`fvSchemes` and `fvSolution` are the numerical core of a standard OpenFOAM case. A lot of divergence, oscillation, and nonphysical behavior is not caused by the mesh alone or the solver name alone, but by an incompatible combination of discretization choices and linear-solver/algorithm controls. These two dictionaries should be reviewed as a pair.

## Functional split

### `fvSchemes`

This dictionary defines **how operators are discretized**, including items such as:

- time derivative schemes (`ddtSchemes`)
- gradient schemes (`gradSchemes`)
- divergence schemes (`divSchemes`)
- laplacian schemes (`laplacianSchemes`)
- interpolation schemes (`interpolationSchemes`)
- snGrad schemes (`snGradSchemes`)

In plain terms, `fvSchemes` determines the numerical approximation style.

### `fvSolution`

This dictionary defines **how algebraic systems are solved and coupled**, including items such as:

- linear solver selection for each field
- tolerances and relative tolerances
- relaxation factors
- algorithm controls for SIMPLE, PISO, or PIMPLE
- residual control / convergence-related settings where supported

In plain terms, `fvSolution` determines the iteration machinery wrapped around those discretized equations.

## Why they must be read together

A scheme can be formally higher-order yet too aggressive for a rough mesh, sharp gradients, or poor initialization. A linear solver can be technically valid yet too weakly controlled for that discretization. The right question is not "Is this scheme good?" but "Is this scheme/solver/mesh/physics combination robust enough for this case stage?"

## `fvSchemes`: practical reading frame

### Time discretization

Transient cases often hinge on whether the time scheme is stable and sufficiently accurate for the flow regime. More aggressive choices can improve accuracy but may reduce robustness if time-step control is not disciplined.

### Gradient and divergence schemes

These often dominate stability behavior. Convection terms especially can become a source of oscillation or overshoot if the scheme is too aggressive for the mesh quality or startup state.

### Laplacian and snGrad consistency

Diffusion-related terms depend on gradient handling and mesh quality sensitivity. On non-orthogonal meshes, these choices can interact strongly with correction strategy and convergence rate.

## `fvSolution`: practical reading frame

### Linear solvers per field

Pressure, velocity, energy, and turbulence variables often use different algebraic solvers and preconditioners. Copying one set blindly across fields is a common mistake.

### Tolerances and `relTol`

These determine how tightly each linear solve is driven within an outer iteration loop. Loose settings may save cost but hide poor equation progress; overly strict settings may waste runtime without helping if the outer algorithm is the real bottleneck.

### Under-relaxation

Relaxation factors are one of the main robustness knobs in steady or difficult coupled problems. They can suppress divergence during startup, but excessive damping can make progress painfully slow or mask deeper incompatibilities.

### Algorithm blocks: SIMPLE / PISO / PIMPLE

The chosen solver family determines whether pressure-velocity coupling is managed by SIMPLE, PISO, or PIMPLE-like controls. These blocks should align with the application in `controlDict`; mismatching them is a structural error, not merely a tuning issue.

## Practical review checklist

Before running or diagnosing a case, verify:

1. `fvSchemes` exists and defines the operators actually used by the solver.
2. `fvSolution` contains solver entries for the fields present in the case.
3. Pressure-velocity algorithm blocks match the selected application.
4. Convection schemes are not overly aggressive for the current startup state.
5. Relaxation settings are plausible for the solver type and difficulty level.
6. Linear solver tolerances are neither accidentally trivial nor unrealistically strict.

## Common failure modes

- Using tutorial numerics from a different solver family
- Aggressive convection scheme causing startup oscillation or divergence
- Missing solver entry for a required field
- SIMPLE/PISO/PIMPLE settings inconsistent with the application
- Relaxation factors too weak for a hard steady case
- Chasing mesh issues while the real problem is an unstable numerics setup

## Anti-patterns

- Upgrading to high-order convection everywhere before the baseline run is stable
- Treating `fvSchemes` as accuracy-only and `fvSolution` as performance-only
- Copying numerics dictionaries from internet snippets without checking solver compatibility
- Blaming all divergence on the mesh before auditing scheme and relaxation choices

## Recommendation

- Review `fvSchemes` and `fvSolution` together, never in isolation.
- Start from numerically conservative settings when bootstrapping a new case.
- Increase aggressiveness only after structural correctness and baseline stability are verified.
- Record solver-family-compatible numerics templates for agent reuse rather than one universal template.

## Rationale

- Discretization and iterative solution are tightly coupled in practical stability behavior.
- Conservative initial numerics reduce false negatives when validating a new case.
- Many troubleshooting loops become shorter when the first pass asks whether the numerics are simply too ambitious.

## Applicability limits

- Exact available schemes and algebraic solvers vary across OpenFOAM variants and versions.
- Specialty solvers can require additional blocks or field-specific conventions.
- Final production settings may legitimately differ from robust startup settings.
