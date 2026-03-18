# controlDict Basics

id: official-controlDict-basics
problem_class: setup
confidence: high
source_refs:
- official-openfoam-user-guide-controlDict
- official-openfoam-function-objects

## Why this note exists

`controlDict` is the run orchestration dictionary. It does not define the PDE discretization or linear-solver details; instead, it defines what application runs, how time advances, when output is written, and which runtime utilities or function objects are active. Many cases fail operationally because `controlDict` is copied mechanically without understanding what it is governing.

## Core responsibilities of `controlDict`

A typical `system/controlDict` answers four questions:

1. **What solver/application should be executed?**
2. **How should the run advance in time or pseudo-time?**
3. **When should results be written?**
4. **What runtime monitoring/post-processing should be executed?**

## High-value entries to understand

### `application`

This points to the solver executable, for example `icoFoam`, `simpleFoam`, or `pimpleFoam`.

If this is wrong, the rest of the case structure is evaluated against the wrong solver family, which cascades into missing-field and incompatible-dictionary errors.

### Time-window control

Common entries include:

- `startFrom`
- `startTime`
- `stopAt`
- `endTime`
- `deltaT`

These define where the run starts, when it ends, and the nominal time step. For steady solvers, time may represent iteration-like progression rather than physical time, but the control mechanism is still handled here.

### Output control

Common entries include:

- `writeControl`
- `writeInterval`
- `purgeWrite`
- `writeFormat`
- `writePrecision`
- `writeCompression`
- `timeFormat`
- `timePrecision`

These control storage behavior. Poor choices here can produce either too little diagnostic output or excessive disk churn.

### Runtime adjustability

Typical entries:

- `adjustTimeStep`
- `maxCo`
- `maxDeltaT`

For transient cases, adaptive time-step control is often essential. Turning it off in aggressive flows can destabilize the run; turning it on without understanding the Courant target can make runs unexpectedly slow.

### Runtime hooks and monitoring

Function objects may be embedded here to calculate residuals, forces, probes, field averages, sampled data, and other diagnostics.

This matters because a good agent should use `controlDict` not only to run a case, but also to make it observable.

## Operational distinctions that matter

### Steady vs transient usage

- In transient runs, `deltaT`, `adjustTimeStep`, and Courant limits directly affect physical time integration.
- In steady runs, time-like progression still controls write cadence and iteration accounting, but the numerical meaning differs.

### Restart behavior

`startFrom` determines whether the solver starts from `startTime`, latest written time, or another chosen state. This is critical when resuming interrupted jobs or running parameter sweeps.

### Post-processing integration

Function objects in `controlDict` let a case emit diagnostics while it runs. This is preferable to flying blind and checking only end-state files.

## Practical review checklist

Before a run, verify:

1. `application` matches the intended solver.
2. Time controls make sense for steady vs transient intent.
3. Output intervals are neither too sparse nor excessively expensive.
4. Adaptive time-step settings are compatible with transient stability expectations.
5. Restart policy (`startFrom`) matches the intended workflow.
6. Function objects are present when runtime observability is important.

## Common failure modes

- Wrong `application` copied from another tutorial
- `deltaT` too large for transient stability
- `writeInterval` so large that debugging data is missing
- `adjustTimeStep yes` with poor `maxCo` expectations, leading to unexpectedly tiny time steps
- Resuming from stale latest time unintentionally
- No residual/probe function objects, making diagnosis harder than necessary

## Anti-patterns

- Treating `controlDict` as just a launch file
- Copying transient time controls into a steady workflow without review
- Ignoring write and monitoring settings until after a failure
- Assuming runtime controls are harmless because they do not look like equation settings

## Recommendation

- Validate `application` first; it anchors the rest of case review.
- Separate physical setup questions from run-orchestration questions; `controlDict` handles the latter.
- For transient cases, review `deltaT`, `adjustTimeStep`, and `maxCo` together.
- Add observability early via function objects, not only after failures occur.

## Rationale

- `controlDict` connects case intent to actual execution behavior.
- Small orchestration mistakes can waste significant compute time even when the physics dictionaries are otherwise correct.
- Good runtime observability shortens troubleshooting loops dramatically.

## Applicability limits

- Exact supported entries and defaults vary across OpenFOAM variants and versions.
- Some workflows split function-object configuration through includes or external files.
- HPC job scripts still control resources outside OpenFOAM; `controlDict` only governs in-application behavior.
