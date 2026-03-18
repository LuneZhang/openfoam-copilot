# Case Structure Overview

id: official-case-structure-overview
problem_class: setup
confidence: high
source_refs:
- official-openfoam-user-guide-case-structure
- official-openfoam-tutorial-conventions

## Why this note exists

OpenFOAM cases are not just folders with arbitrary files. Most setup failures happen because required dictionaries are missing, placed in the wrong directory, named incorrectly, or written for the wrong physics/solver family. A reliable agent needs a canonical mental model of the standard case anatomy before touching numerics or turbulence.

## Canonical directory anatomy

A minimal OpenFOAM case usually revolves around three top-level directories:

- `0/`: initial and boundary conditions for solved fields at start time.
- `constant/`: physical properties and mesh-related data that are normally time-invariant.
- `system/`: run control, discretization, linear-solver, and workflow dictionaries.

This is the backbone. Even when tutorials add extra files, they normally extend this pattern rather than replace it.

## What normally lives in each directory

### `0/`

This directory contains field files such as:

- `U`
- `p` or `p_rgh`
- `T`
- turbulence fields such as `k`, `epsilon`, `omega`, `nut`, `nuTilda`
- phase fraction or species fields when the chosen solver requires them

Key rule: files in `0/` must match the fields actually solved or required by the selected solver and model set. Missing a required field often causes immediate startup failure. Adding fields that the solver never uses is less catastrophic, but creates confusion and review noise.

### `constant/`

Typical contents include:

- `polyMesh/` for mesh files
- `transportProperties`
- `turbulenceProperties`
- `thermophysicalProperties`
- gravity file `g` in buoyant or multiphase contexts
- region/material property dictionaries for more advanced setups

Key rule: `constant/` is where case-wide physics assumptions live. If a case changes from incompressible to compressible, or from laminar to RANS, this directory usually changes with it.

### `system/`

Typical contents include:

- `controlDict`
- `fvSchemes`
- `fvSolution`
- `blockMeshDict` or meshing workflow dictionaries
- `decomposeParDict` for parallel runs
- function object definitions when embedded in `controlDict` or separate includes

Key rule: `system/` controls *how* the equations are run, not the physical fields themselves.

## Solver-dependent variation

A correct case structure is solver-specific, not universal. For example:

- incompressible solvers often expect `p` and `U`
- buoyant solvers may expect `p_rgh`, `T`, and gravity-related setup
- turbulence-enabled cases require extra model fields depending on the chosen closure
- multiphase and reacting solvers can add many more field and property dictionaries

Therefore, case validation should always start with: "Which solver is this case built for?" The directory tree can only be judged relative to that answer.

## Practical review checklist

Before running a case, verify:

1. The chosen solver is explicit and matches the intended physics.
2. `system/controlDict` names the intended application.
3. `0/` contains all required primary and model-dependent fields.
4. `constant/` contains the matching property dictionaries for the solver family.
5. `system/fvSchemes` and `system/fvSolution` exist and are not copied from an incompatible tutorial.
6. Mesh files or mesh-generation dictionaries exist and are consistent with the workflow.
7. Parallel dictionaries are present if the run plan requires decomposition.

## Common failure modes

- Missing required field file in `0/`
- Using `p` where the solver expects `p_rgh`, or the reverse
- Copying `turbulenceProperties` without the required turbulence fields
- Reusing `fvSchemes`/`fvSolution` from a different solver family
- Forgetting gravity `g` for buoyant configurations
- Putting a dictionary under the wrong directory, so OpenFOAM cannot locate it

## Anti-patterns

- Treating case folders as generic templates independent of solver choice
- Blindly copying a tutorial and deleting files until startup errors stop
- Editing only `0/` and ignoring whether `constant/` still matches the physics
- Assuming all cases use the same pressure variable conventions

## Recommendation

- Use the `0/` / `constant/` / `system/` triad as the first-pass validation frame.
- Review case structure solver-first, not file-first.
- When building templates for agents, encode required-vs-optional files by solver family.
- Record common directory mismatches as setup errors rather than numerics errors.

## Rationale

- Most startup failures are structural before they are numerical.
- OpenFOAM dictionaries are distributed by responsibility; understanding that distribution reduces copy-paste mistakes.
- A stable agent workflow needs deterministic pre-run checks, and case structure is the highest-leverage early check.

## Applicability limits

- Advanced multi-region or custom-solver cases can add nonstandard dictionaries.
- Some packaged tutorials use includes, generated files, or helper scripts that reduce visible files in the base tree.
- Exact file names can vary across solver families and OpenFOAM distributions.
