# Troubleshooting Node — Thermo / Chemistry Package Inconsistency

id: thermo-chemistry-package-inconsistency
symptom: Thermal, compressible, or reacting cases show nonphysical temperature/density/species behavior or repeated instability that survives simple numerics damping.

probable_causes:
- `thermophysicalProperties` inconsistent with the solver family
- chemistry / species dictionaries mismatched to the reacting branch
- temperature, pressure, and species fields initialized or constrained inconsistently
- a compressible/reacting case derived from an incompressible template without a full thermo reset

first_checks:
- verify the chosen solver family truly expects the current thermo/chemistry package
- inspect `thermophysicalProperties` for internal coherence with the intended physics branch
- verify required species and thermal fields exist and have coherent BCs
- check whether the case was copied from a mismatched tutorial family

deeper_checks:
- compare against the nearest official thermal/reacting tutorial family
- inspect whether apparent BC instability is really property-model inconsistency
- inspect whether chemistry complexity was added before the baseline thermo branch was stable

likely_fixes:
- replace the thermo/chemistry package with one coherent for the chosen branch
- rebuild thermal/species field initialization on physically plausible scales
- validate the non-reacting or simpler thermo baseline before reintroducing full chemistry detail

escalation_path:
- if the thermo package is coherent but instability remains, branch into Courant-driven-transient-instability, turbulence-field-startup-mismatch, or mesh-quality-driven-instability

source_refs:
- official-openfoam-thermophysical-properties
- official-openfoam-compressible-setup-guidance
- official-openfoam-tutorial-catalog

confidence: high
notes:
- In thermal/reacting cases, property-model inconsistency can look like a numerics problem for a long time.
