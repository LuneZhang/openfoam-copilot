# Divergence Recovery v1

## Goal
Provide a prioritized recovery workflow for OpenFOAM cases that diverge, blow up, or produce clearly unstable behavior.

## Scope
Use this playbook for symptoms such as:
- residual blow-up
- floating point exception
- continuity error growth
- rapidly increasing Courant number
- obvious nonphysical field values

Do not treat this as a flat checklist. Follow the order.

## Phase 1 — Classify the symptom precisely
Before changing anything, record:
- exact solver/application
- exact symptom
- when it happens (immediate startup / after some iterations / after mesh or timestep change / only in parallel)
- whether the failure is serial, parallel, or both

This prevents random parameter thrashing.

## Phase 2 — Clear structural setup first
Check:
1. Is the selected solver family correct for the physics?
2. Are the required fields present under `0/`?
3. Are the property dictionaries under `constant/` consistent with the solver family?
4. Do patch names match the mesh?
5. Is the pressure variable convention correct (`p` vs `p_rgh` where applicable)?

If any of these are wrong, stop numerical tuning and fix them first.

## Phase 3 — Review boundary conditions as a coupled system
Check:
1. Are velocity and pressure boundary conditions complementary?
2. Are outlet/inlet/wall choices physically reasonable?
3. If turbulence is enabled, are all turbulence-field BCs present and consistent?
4. If heat transfer or buoyancy is involved, are thermal/gravity-related BCs coherent?

If BC structure is wrong, numerics tuning is usually wasted effort.

## Phase 4 — Check the mesh
Run `checkMesh` and classify findings into:
- fatal structural issues
- severe quality issues
- manageable warnings

Priorities:
1. eliminate fatal issues
2. locate worst cells, not just average statistics
3. ask whether worst cells overlap with critical physics regions

If severe mesh issues align with instability symptoms, prefer mesh improvement over endless damping.

## Phase 5 — Reduce numerical aggressiveness
Only after structure, BCs, and mesh are reviewed, move to numerics.

Default recovery moves:
1. make convection treatment more conservative
2. verify SIMPLE/PISO/PIMPLE block matches the application
3. reduce startup aggressiveness
4. strengthen relaxation where appropriate
5. check linear solver settings and tolerances

Principle:
- first restore robustness
- then recover accuracy later

## Phase 6 — Reduce startup risk
Check runtime control and initialization:
1. reduce `deltaT`
2. use `adjustTimeStep` / `maxCo` sensibly where appropriate
3. inspect startup field magnitudes for obviously unreasonable values
4. ensure restart state is suitable and not stale/corrupted for the new configuration

This phase is especially important when the case survives a little while before diverging.

## Phase 7 — Re-evaluate model/physics fit
If the case still diverges after the previous phases, ask:
1. Is the solver family fundamentally wrong?
2. Is the turbulence model inappropriate for the setup stage?
3. Is the case being treated as steady when it should be transient?
4. Is a compressible/thermal/multiphase framing missing where it should exist?

Do not assume the model family is correct just because the geometry looks familiar.

## Phase 8 — Parallel-specific recovery
If the failure is mainly visible in parallel:
1. verify whether the serial case is sane
2. review `decomposeParDict`
3. inspect per-processor logs
4. separate decomposition problems from real solver instability

Parallel debugging should not hide upstream structural problems.

## High-confidence recovery pattern
When a case is exploding and root cause is unclear, the safest default recovery order is:
1. confirm solver family
2. confirm field/property structure
3. confirm BC consistency
4. run `checkMesh`
5. make numerics conservative
6. reduce timestep/startup aggressiveness
7. retry in serial if practical

## Anti-patterns
- changing mesh, BCs, numerics, and timestep all at once
- trying relaxation-factor tweaks before checking structure
- blaming turbulence model first in every case
- treating `checkMesh` warnings as optional trivia
- debugging a broken serial case only in parallel

## Output behavior for agents
When using this playbook, the agent should report:
1. symptom classification
2. top likely error class
3. first three checks to run now
4. fixes already justified by evidence
5. next escalation step if the first fixes do not work

## Recommended Scenario Families

- `buoyant-natural-convection-room-scale`
- `compressible-thermo-flow-generic`
- `multiphase-interface-flow-generic`
- `reacting-combustion-flow-generic`
- `incompressible-rans-external-aerodynamics`

## Primary Troubleshooting Node Handoffs

- `floating-point-exception-startup`
- `continuity-error-growth`
- `mesh-quality-driven-instability`
- `courant-driven-transient-instability`
- `steady-state-divergence-overaggressive-numerics`
