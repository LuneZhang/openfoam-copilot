# Troubleshooting Node — Steady-State Divergence from Overaggressive Numerics

id: steady-state-divergence-overaggressive-numerics
symptom: Residuals or monitored quantities blow up during early steady-state iterations after switching to aggressive convection schemes or high relaxation factors.

probable_causes:
- relaxation factors set too high for the case maturity and coupling strength
- higher-order convection used before the baseline flow field is stable
- steady-state chosen for a case with strongly transient startup behavior
- structural issues in BCs or mesh being masked until numerics become less forgiving

first_checks:
- revert to conservative startup numerics before making more changes
- inspect current relaxation factors and compare them against a bounded practical range
- check whether the solver family should really be transient or pseudo-transient during startup
- confirm BC and mesh sanity so numerics are not covering for structural mistakes

deeper_checks:
- compare current `fvSchemes` against a known conservative tutorial baseline
- inspect whether residual blow-up is tied to a specific equation or begins everywhere at once
- review whether turbulence or buoyancy coupling adds startup stiffness that steady-state settings cannot absorb cleanly

likely_fixes:
- reduce manual relaxation into a conservative range instead of oscillating between extremes
- replace higher-order convection with upwind or bounded-upwind for startup stabilization
- use a transient/pseudo-transient startup path, then restore sharper numerics after the field settles
- fix BC or mesh issues before reintroducing aggressive numerics

escalation_path:
- if conservative numerics still diverge, branch into BC mismatch, mesh-quality, or wrong-solver-family diagnosis rather than continuing parameter thrash

source_refs:
- community-simscale-docs-relaxation-factors
- community-simscale-kb-floating-point-exception
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

confidence: medium
notes:
- This node is about bounded startup heuristics, not final accuracy settings.
- Low relaxation can buy stability but cannot rescue a fundamentally wrong case definition.
