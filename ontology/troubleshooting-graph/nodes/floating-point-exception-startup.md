# Troubleshooting Node — Floating Point Exception at Startup

id: floating-point-exception-startup
symptom: Solver aborts early with a floating point exception, often within initial iterations or immediately after launch.

probable_causes:
- nonphysical zero or near-zero initial/boundary values for active fields required by the chosen solver branch
- pressure-variable mismatch, especially compressible pressure setup or buoyancy-specific pressure conventions
- timestep too large for the startup transient or Courant jump
- aggressive convection schemes that destabilize a not-yet-settled case
- mesh or boundary-condition inconsistency severe enough to trigger numerical blow-up

first_checks:
- verify solver family and active field set are correct for the intended physics branch
- inspect initial and boundary values for pressure, temperature, and turbulence variables for nonphysical placeholders
- confirm whether the case uses `p` or `p_rgh` and whether reference-pressure treatment is coherent
- reduce startup timestep / tighten Courant control before touching advanced tuning
- switch to conservative upwind or bounded-upwind convection only as a bounded fallback

deeper_checks:
- run `checkMesh` and classify whether quality problems are severe enough to explain immediate failure
- compare the case against the nearest official tutorial pattern for missing dictionaries or BC roles
- inspect `fvSolution` and coupling controls only after field set and BC logic are confirmed
- check whether the crash appears only after parallel decomposition, which would suggest an additional decomposition or patch issue

likely_fixes:
- replace zero or placeholder values with physically plausible startup values
- correct pressure/reference-pressure treatment for compressible or buoyant branches
- lower timestep or add tighter adaptive timestep limits during startup
- temporarily downgrade convection schemes to stability-first choices
- repair structural BC or mesh issues before revisiting relaxation factors

escalation_path:
- if the case still fails, classify the problem by branch: compressible pressure issue, buoyancy convention issue, turbulence-field issue, mesh issue, or parallel-only issue
- create a branch-specific node once repeated evidence accumulates for a narrower failure signature

source_refs:
- community-simscale-kb-floating-point-exception
- community-simscale-forum-floating-point-thread
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

confidence: medium
notes:
- Treat floating point exception as a symptom bucket, not a single diagnosis.
- Relaxation-factor changes are intentionally not the first line here.
