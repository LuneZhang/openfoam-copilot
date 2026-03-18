# Mesh Quality Repair v1

## Goal
Provide a first-pass repair workflow when mesh quality is suspected to be driving instability.

## Step 1 — Confirm mesh is part of the problem
Run `checkMesh` and classify findings:
- fatal structural errors
- severe quality issues
- manageable warnings

If fatal issues exist, repair the mesh before meaningful solver tuning.

## Step 2 — Locate the worst cells
Do not rely only on global counts. Identify whether the worst-quality cells lie in:
- near-wall layers
- separation zones
- inlets/outlets
- interfaces
- strong heat-release or high-gradient regions

Local bad cells in critical regions matter more than average quality statistics.

## Step 3 — Correlate mesh symptoms with solver symptoms
Ask:
- do residual explosions begin where poor cells are likely to matter?
- does the case become stable only when numerics are made extremely conservative?
- do pressure/gradient-related issues dominate?

These clues often point to mesh-driven instability.

## Step 4 — Choose repair path by severity
### Fatal structural issues
- regenerate or repair the mesh before further debugging

### Severe quality issues
- consider local remeshing or global mesh strategy changes
- reduce numerical aggressiveness while evaluating repair impact

### Manageable warnings
- keep the mesh if justified, but compensate with conservative startup numerics and tighter runtime control

## Step 5 — Avoid fake fixes
These actions can hide a bad mesh without solving it:
- excessive relaxation used forever
- extreme timestep reduction without root-cause review
- blaming turbulence model before inspecting cell quality hotspots

## Step 6 — Re-run with explicit comparison
After repair or mitigation, compare:
- `checkMesh` severity class
- residual pattern changes
- stability margin changes
- whether the same failure mode persists

## Recommendation
- Use mesh repair when quality issues align with instability symptoms.
- Treat severe mesh issues as structural risk, not as an optional cleanup task.
- Distinguish between “mesh must be rebuilt” and “mesh is imperfect but manageable with conservative settings.”

## Output behavior for agents
When recommending mesh repair, report:
1. mesh issue class (fatal / severe / manageable)
2. likely numerical consequence
3. whether conservative numerics are a temporary workaround or not enough
4. the next repair decision in priority order

## Recommended Scenario Families

- `incompressible-rans-external-aerodynamics`
- `buoyant-natural-convection-room-scale`
- `compressible-thermo-flow-generic`
- `multiphase-interface-flow-generic`
- `reacting-combustion-flow-generic`

## Primary Troubleshooting Node Handoffs

- `mesh-quality-driven-instability`
- `critical-region-local-mesh-hotspot`
- `floating-point-exception-startup`
- `continuity-error-growth`
- `courant-driven-transient-instability`
