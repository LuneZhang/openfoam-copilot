# Solver Family Overview

id: official-solver-family-overview
problem_class: setup
confidence: high
source_refs:
- official-openfoam-user-guide-solver-selection
- official-openfoam-tutorial-catalog

## Why this note exists

Solver choice is the first major branch in an OpenFOAM workflow. If the wrong solver family is chosen, every downstream dictionary review becomes noisy: the wrong fields appear missing, the wrong property dictionaries are expected, and numerics copied from tutorials start fighting the problem statement. Agents need a coarse but dependable solver-family map before fine-grained setup advice makes sense.

## Primary selection axes

A practical first-pass solver selection usually asks:

1. Is the flow **incompressible** or **compressible**?
2. Is the target run mainly **steady** or **transient**?
3. Is the case **single-phase** or **multiphase**?
4. Is there **heat transfer**, **buoyancy**, **combustion**, or **species transport**?
5. Is the turbulence treatment **laminar**, **RANS**, or **LES**?

OpenFOAM solver names encode these choices imperfectly, so reading a tutorial catalog and solver description matters more than guessing from one keyword.

## Coarse family map

### Incompressible single-phase

Typical examples include transient and steady solvers for Newtonian flow. These are often the cleanest entry point for learning standard `U`/`p` workflows and SIMPLE/PISO/PIMPLE-style coupling.

Good for:

- baseline external/internal flow setups
- numerics and boundary-condition learning
- separating structural errors from advanced-physics complexity

### Compressible / thermal flow

These add energy and thermophysical coupling. Cases usually require additional property dictionaries and more careful variable conventions.

Good for:

- high-speed flow
- significant density variation
- heat-transfer or thermo-coupled setups

### Buoyant flow

These commonly introduce gravity-driven coupling and often use pressure formulations like `p_rgh` instead of plain `p`.

Good for:

- natural convection
- mixed buoyancy/forced-convection problems
- thermal stratification contexts

### Multiphase

These add phase fraction fields, interfacial models, and more complex stability concerns.

Good for:

- free-surface problems
- dispersed phases
- interface-capturing or phase-interaction cases

### Reacting / combustion / species transport

These can involve chemistry, heat release, species equations, thermo packages, and sometimes turbulence-chemistry interaction complexity.

Good for:

- flames and reacting systems
- combustion research workflows
- species-sensitive transport studies

## Why family choice matters structurally

Different solver families change:

- required field names under `0/`
- required property dictionaries under `constant/`
- pressure variable conventions
- valid algorithm blocks in `fvSolution`
- expected function-object diagnostics
- the meaning of a "reasonable" startup numerics setup

That is why a generic "OpenFOAM template" is often misleading. Templates should be grouped by solver family and use case.

## Practical solver-selection workflow

When bootstrapping a case:

1. Start from the physics statement, not from a favorite solver name.
2. Identify the closest official tutorial family.
3. Reuse the tutorial’s structural pattern before customizing details.
4. Only then adapt numerics, turbulence, and runtime controls.

For agent workflows, the most useful approach is to maintain a mapping from problem traits to representative official tutorials and solver families.

## Common failure modes

- Choosing an incompressible solver for a thermo-dominated problem
- Using a steady solver workflow where transient evolution is central
- Missing `p_rgh`-style pressure treatment in buoyant cases
- Copying single-phase setup logic into a multiphase case
- Treating solver choice as a small implementation detail rather than the main setup branch

## Anti-patterns

- Selecting a solver only because its name looks familiar
- Forcing one favorite solver across unrelated physics classes
- Mixing dictionaries from tutorials belonging to different solver families
- Tuning numerics for days before confirming solver-family fit

## Recommendation

- Put solver-family identification at the top of every case review.
- Organize future project knowledge by family, not by arbitrary keyword lists.
- Use official tutorial lineage as the default evidence base for initial templates.
- Treat solver mismatch as a setup-class error that must be resolved before numerics tuning.

## Rationale

- Solver choice determines what "correct case structure" even means.
- Early family alignment removes many false troubleshooting branches.
- Official tutorials provide the most reliable starting patterns for each family.

## Applicability limits

- Exact solver names and availability differ across OpenFOAM forks and releases.
- Some custom research solvers combine behaviors across standard families.
- Final solver selection may still require domain expertise beyond a coarse family map.
