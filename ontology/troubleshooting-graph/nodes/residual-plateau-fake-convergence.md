# Troubleshooting Node — Residual Plateau / Fake Convergence

id: residual-plateau-fake-convergence
symptom: Residuals stop decreasing or appear numerically quiet, but the solution remains physically suspicious, drifted, or clearly not yet trustworthy.

probable_causes:
- solver tolerances or relative tolerances are masking weak progress
- the run is stable numerically but trapped in a poor setup state
- steady-state assumptions are being forced on a case with genuinely unsteady behavior
- key monitored physical quantities are not actually converged even though residuals look calm

first_checks:
- identify whether the case is intended to be steady or transient
- compare residual behavior with monitored physical quantities, not residuals alone
- inspect field-specific solver stopping criteria in `fvSolution`
- check whether boundary conditions or initialization imply a biased but numerically quiet solution

deeper_checks:
- compare against a conservative baseline or shorter controlled rerun
- inspect whether only one field is plateauing while others drift
- verify that the selected solver family matches the intended physics and temporal behavior

likely_fixes:
- tighten convergence criteria where weak tolerances are hiding poor progress
- use additional monitors / probes / integrated quantities instead of residuals alone
- revisit solver family or transient/steady framing if the case is physically unsteady
- fix structural setup issues before celebrating numerical quietness

escalation_path:
- if residuals remain flat and physical monitors stay wrong, branch into wrong-solver-family-selection, BC mismatch, or initialization-driven bias

source_refs:
- official-openfoam-user-guide-fvSolution
- official-openfoam-function-objects
- community-simscale-docs-relaxation-factors

confidence: high
notes:
- Quiet residuals are not proof of a correct solution.
