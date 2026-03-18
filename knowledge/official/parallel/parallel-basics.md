# Parallel Execution Basics

id: official-parallel-basics
problem_class: execution
confidence: high
source_refs:
- official-openfoam-user-guide-parallel
- official-openfoam-decomposePar-guide

## Why this note exists

OpenFOAM parallel execution is not just a speed feature; it changes the operational workflow and adds a new class of setup and debugging failures. Agents need a baseline model of decomposition, per-processor execution, and reconstruction in order to separate solver problems from parallel workflow problems.

## Canonical parallel workflow

A standard parallel workflow often looks like:

1. prepare a valid serial case
2. define `decomposeParDict`
3. run `decomposePar`
4. launch the solver in parallel
5. inspect per-processor behavior and logs
6. reconstruct results if needed

The most important rule is: **parallel execution should start from a structurally valid serial case**. If a case is already broken in serial, parallelism usually amplifies confusion rather than helping.

## What `decomposeParDict` controls

This dictionary defines how the case is split into processor subdomains.

Core concerns include:
- number of subdomains
- decomposition method
- load distribution strategy
- consistency with geometry and hardware intent

A decomposition choice is not purely administrative. Poor decomposition can hurt convergence, increase communication cost, and complicate debugging.

## Why parallel runs fail differently

Parallel runs add new failure classes:

- decomposition dictionary missing or inconsistent
- decomposition incompatible with the intended processor count
- patch/region/file inconsistencies after decomposition
- per-processor divergence not obvious from short console summaries
- reconstruction or post-processing confusion

## Practical review checklist

Before launching in parallel, verify:

1. The case runs or at least initializes correctly in serial.
2. `decomposeParDict` exists and matches the intended processor count.
3. The decomposition method is plausible for the geometry and case scale.
4. The workflow for decompose -> run -> reconstruct is explicit.
5. Logs can be inspected per processor if something goes wrong.
6. Any function objects or output assumptions still make sense in parallel.

## Common failure modes

- launching with a processor count inconsistent with decomposition settings
- debugging a fundamentally broken serial case only in parallel
- losing visibility because all processors write noisy logs simultaneously
- reconstructing incorrectly and misreading output state
- interpreting communication/parallel errors as purely numerics errors

## Anti-patterns

- using parallel as the first test of a fresh case
- changing decomposition and numerics simultaneously, making failures hard to localize
- assuming a successful decomposition guarantees a stable parallel run
- forgetting that processor-local errors can expose structural issues hidden in serial shortcuts

## Recommendation

- Validate the serial case first whenever practical.
- Treat decomposition settings as part of case setup, not an afterthought.
- Keep the decomposition workflow explicit in playbooks and checklists.
- When a parallel case fails, first classify whether the failure is structural, decomposition-related, or genuine solver instability.

## Rationale

- Parallel execution adds operational complexity and a distinct error surface.
- Clear serial-first and decomposition-aware workflows reduce false diagnosis.
- Agents need an explicit model of the execution pipeline to debug parallel cases effectively.

## Applicability limits

- Exact commands and MPI launch details depend on environment and OpenFOAM distribution.
- Some large cases may require parallel-first workflow for practical reasons, but the serial-validity principle still matters conceptually.
- HPC scheduler integration lies partly outside OpenFOAM dictionary semantics.
