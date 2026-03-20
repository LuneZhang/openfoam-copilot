# Troubleshooting Node — Premixed Ignition or Flame-Speed Model Mismatch

id: premixed-ignition-or-flame-speed-model-mismatch
symptom: A premixed combustion case reaches the right broad solver family, but startup still fails because ignition framing, flame-speed modeling, or premixed flame-structure fields are not coherently defined.

probable_causes:
- required premixed ignition, flame-speed, progress-variable, or burned-fraction fields are missing or initialized incoherently
- ignition structure is too loose or physically inconsistent for the premixed branch
- a nonpremixed or generic reacting setup was copied into a premixed XiFoam-style case
- startup numerics are being blamed before the premixed branch itself is structurally valid

first_checks:
- confirm the case really belongs to a premixed branch rather than a diffusion-flame, spray, or generic reacting branch
- verify the required premixed ignition, flame-speed, progress-variable, and flame-structure fields exist and are initialized coherently
- compare ignition and premixed field setup against the nearest official premixed tutorial lineage
- verify thermo and boundary conditions as one coupled premixed system before wider numerics changes

deeper_checks:
- inspect whether the first instability starts in the ignition or flame-anchor region rather than across the whole domain
- compare current startup controls against a conservative premixed baseline rather than a mature target-state setup
- separate true premixed-field mismatch from a deeper thermo package or mesh hotspot problem

likely_fixes:
- rebuild the premixed field and ignition structure from the nearest premixed tutorial baseline
- keep startup controls conservative until the premixed branch behaves coherently
- if the case is not actually premixed, leave this node and return to a more suitable combustion family

escalation_path:
- if the case is not truly premixed, route to `wrong-solver-family-selection`
- if thermo is inconsistent, route to `thermo-chemistry-package-inconsistency`
- if a local region is driving the failure, route to `critical-region-local-mesh-hotspot`

source_refs:
- official-openfoam-xifoam-guide
- official-openfoam-tutorial-premixed-combustion-xifoam
- official-openfoam-thermophysical-properties
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

confidence: medium
notes:
- Use this node only after the case is already narrow enough to call it premixed.
- This node exists so agents do not hide premixed ignition or flame-speed-model problems inside the generic reacting startup branch.
