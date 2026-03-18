# First-Pass Case Setup Checklist

## Goal
Provide an ordered setup workflow that an agent should use before deeper tuning.

## Step 1 — State the problem correctly
Write down:
- physics class
- steady or transient intent
- incompressible or compressible intent
- single-phase or multiphase intent
- whether heat transfer, buoyancy, or chemistry matters

If this statement is fuzzy, stop and clarify before touching dictionaries.

## Step 2 — Choose the solver family first
- identify the likely solver family
- find the nearest official tutorial pattern
- do not start from a generic case template with unclear lineage

## Step 3 — Validate case structure
Check that the case follows the `0/`, `constant/`, `system/` pattern.
Verify:
- primary fields exist
- model-dependent fields exist
- property dictionaries match the chosen solver family
- `controlDict`, `fvSchemes`, and `fvSolution` exist

## Step 4 — Review boundary conditions as a coupled system
Do not review `U`, `p`, turbulence fields, and thermal fields independently.
Check:
- patch names match the mesh
- pressure/velocity BCs are complementary
- turbulence fields are present and consistent if turbulence is enabled
- thermal or buoyancy fields are included where required

## Step 5 — Review numerics conservatively
For a fresh case:
- prefer conservative startup numerics
- avoid overly aggressive convection choices initially
- ensure algorithm block matches the solver family
- ensure linear solver entries exist for active fields

## Step 6 — Review runtime control
Check `controlDict` for:
- correct `application`
- sensible start/end policy
- sensible `deltaT`
- output cadence useful for debugging
- adaptive timestep controls where appropriate
- runtime observability (residuals/probes/function objects)

## Step 7 — Check the mesh early
Run and interpret `checkMesh` before blaming numerics.
Classify findings as:
- fatal structural issue
- severe quality issue
- manageable warning

## Step 8 — Decide serial-first vs parallel-ready
Default rule:
- validate the case in serial first when practical
- only then move to `decomposeParDict` and parallel execution

## Step 9 — Define startup risk level
Before first serious run, classify the case as:
- low risk
- medium risk
- high risk

Risk rises when you have:
- poor mesh quality
- aggressive numerics
- strong coupling
- multiphase or reacting physics
- uncertain BCs
- large `deltaT`

## Step 10 — Only then start debugging or tuning
Do not jump straight to relaxation-factor tuning or mesh blame unless Steps 1–9 are already checked.

## Output behavior for agents
When using this checklist, the agent should report:
1. solver-family choice and rationale
2. structural issues found
3. boundary-condition risks
4. numerics risks
5. mesh risks
6. the top three fixes or next checks in priority order

## Recommended Scenario Families

- `incompressible-laminar-internal-flow`
- `incompressible-rans-external-aerodynamics`
- `buoyant-natural-convection-room-scale`
- `compressible-thermo-flow-generic`
- `multiphase-interface-flow-generic`
- `reacting-combustion-flow-generic`

## Primary Troubleshooting Node Handoffs

- `wrong-solver-family-selection`
- `patch-name-boundary-mismatch`
- `p-vs-p_rgh-confusion`
- `turbulence-field-startup-mismatch`
- `thermo-chemistry-package-inconsistency`
