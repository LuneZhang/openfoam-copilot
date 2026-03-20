# Troubleshooting Node — Nonpremixed Mixture-Fraction or Stoichiometric Inlet Mismatch

id: nonpremixed-mixture-fraction-or-stoichiometric-inlet-mismatch
symptom: A diffusion-flame or nonpremixed case destabilizes because fuel and oxidizer stream definition, stoichiometric inlet framing, mixture-fraction assumptions, or reverse-flow composition is structurally inconsistent.

probable_causes:
- fuel and oxidizer stream states are defined inconsistently across velocity, temperature, and species fields
- reverse-flow-capable outlets or openings feed undefined or unphysical return-state composition
- a generic reacting template was reused without a true separated-stream audit
- the case is being treated as chemistry stiffness before the stream structure is proven

first_checks:
- verify the case really belongs to a nonpremixed or diffusion-flame branch rather than a premixed branch
- inspect fuel and oxidizer species BCs together as one coupled stream definition with explicit stoichiometric inlet intent
- inspect reverse-flow and outlet treatment for meaningful species and thermal return state
- compare stream definitions against the nearest official reactingFoam diffusion-flame tutorial lineage

deeper_checks:
- inspect whether the first instability appears at one stream boundary or a recirculating outlet rather than in the bulk flame zone
- separate stream-definition mismatch from a deeper thermo package or mesh hotspot problem
- compare startup controls against a conservative reacting baseline only after stream structure is coherent

likely_fixes:
- rebuild stream species and temperature BCs from the nearest diffusion-flame tutorial baseline
- make reverse-flow state treatment explicit at outlets or openings that can recirculate
- if the branch is actually premixed or spray-driven, leave this node and route accordingly

escalation_path:
- if the real issue is reverse-flow role confusion, route to `outlet-backflow-role-confusion`
- if thermo is inconsistent, route to `thermo-chemistry-package-inconsistency`
- if a local region is driving the failure, route to `critical-region-local-mesh-hotspot`

source_refs:
- official-openfoam-reactingfoam-guide
- official-openfoam-tutorial-nonpremixed-diffusion-reactingfoam
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-docs-inletOutlet-backflow
- community-cfd-online-reactingfoam-diffusion-flame-thread

confidence: medium
notes:
- This node exists because separated-stream combustion has a distinct stoichiometric and mixture-fraction first-check order that the generic reacting branch does not capture well.
