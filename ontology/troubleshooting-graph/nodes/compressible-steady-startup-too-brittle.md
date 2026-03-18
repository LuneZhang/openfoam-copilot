# Troubleshooting Node — Compressible Steady Startup Too Brittle

id: compressible-steady-startup-too-brittle
symptom: A compressible thermo case diverges or behaves violently during early steady-state startup, while the main evidence suggests the case may be structurally coherent but too stiff for an immediate steady solve.

probable_causes:
- the case is being forced into a steady compressible solve before pressure, temperature, and density fields have a stable coupled baseline
- startup numerics are too ambitious for a tightly coupled thermo-compressible branch
- the case would benefit from transient or pseudo-transient stabilization before attempting a steady workflow
- local high-gradient regions or fragile BC coupling make early steady residual control misleadingly brittle
- the solver family is nominally plausible, but startup intent is too aggressive for the current field state

first_checks:
- confirm the case is truly intended to end as steady-state, not merely assumed steady because that looks cheaper
- verify solver-family fit and `thermophysicalProperties` coherence before blaming the steady strategy alone
- inspect whether pressure and thermal BCs are physically coupled in a plausible way for the compressible branch
- check whether one local hotspot or high-gradient region is destabilizing the startup before the global field settles
- compare the current startup path against a more conservative transient or pseudo-transient tutorial lineage for the same problem family

deeper_checks:
- inspect whether residual blow-up occurs immediately, which often indicates startup brittleness rather than late-stage convergence failure
- compare current `fvSchemes` / `fvSolution` against a conservative compressible baseline rather than a mature production steady setup
- separate true steady-startup brittleness from cases where solver family or thermo package is actually wrong
- verify that the mesh is not only globally acceptable but also locally robust in high-gradient compressible regions

likely_fixes:
- switch to a conservative transient or pseudo-transient startup path to establish a stable coupled field first
- lower startup aggressiveness in schemes, relaxation, and timestep control before retrying the steady route
- keep the steady target if needed, but only after the field has settled through a safer startup phase
- if structural issues remain, fix thermo, BC, or hotspot problems before retrying steady startup

escalation_path:
- if solver family or thermo package is actually wrong, route to `wrong-solver-family-selection` or `thermo-chemistry-package-inconsistency`
- if the real problem is a local hotspot, route to `critical-region-local-mesh-hotspot`
- if the case remains unstable even under conservative transient startup, route into wider BC / mesh / compressible branch diagnosis rather than insisting on steady settings

source_refs:
- official-openfoam-user-guide-solver-selection
- official-openfoam-compressible-setup-guidance
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution
- community-simscale-docs-relaxation-factors
- community-simscale-kb-floating-point-exception

confidence: medium
notes:
- This node is not an excuse to avoid steady compressible workflows entirely.
- It exists to capture cases where the steady target may be valid, but the immediate startup path is too brittle.
