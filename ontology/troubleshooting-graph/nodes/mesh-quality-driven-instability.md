# Troubleshooting Node — Mesh-Quality-Driven Instability

id: mesh-quality-driven-instability
symptom: The case becomes unstable, highly oscillatory, or sensitive to numerics/timestep changes in a way that strongly suggests the mesh is a primary driver.

probable_causes:
- severe non-orthogonality or skewness
- locally poor cells in critical gradient regions
- marginal mesh being pushed by aggressive numerics
- mesh warnings dismissed even though they correlate with the unstable region

first_checks:
- run `checkMesh`
- classify fatal / severe / manageable mesh issues
- locate where the worst cells are, not just how many exist
- correlate unstable regions with poor-quality cells

deeper_checks:
- compare stability under conservative numerics versus current settings
- inspect whether instability is dominated by pressure/gradient-sensitive equations
- test whether mesh cleanup improves behavior more than relaxation changes do

likely_fixes:
- repair or regenerate the mesh if fatal or severe issues dominate
- temporarily use conservative numerics while validating mesh impact
- prioritize quality improvement near critical flow/thermal/interface regions

escalation_path:
- if the mesh is acceptable after careful review, branch into BC mismatch or solver/model-family mismatch instead of repeatedly damping numerics

source_refs:
- official-openfoam-user-guide-checkMesh
- official-openfoam-mesh-quality-guidance
- community-simscale-kb-floating-point-exception

confidence: high
notes:
- A marginal mesh can mimic many other failure classes; classify it early.
