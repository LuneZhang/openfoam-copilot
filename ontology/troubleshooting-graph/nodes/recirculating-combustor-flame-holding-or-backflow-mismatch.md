# Troubleshooting Node — Recirculating Combustor Flame-Holding or Backflow Mismatch

id: recirculating-combustor-flame-holding-or-backflow-mismatch
symptom: A partially premixed recirculating combustor destabilizes because flame-holding structure, returning mixture state, pilot stream, or reverse-flow treatment is structurally inconsistent.

probable_causes:
- reverse-flow-capable outlets or openings return undefined or unphysical thermal or species state
- pilot and main streams are structurally inconsistent
- a plain premixed template was reused without the extra recirculation-state audit
- the run is being treated as generic reacting stiffness before the recirculating branch is coherent

first_checks:
- confirm the case really belongs to a partially premixed recirculating combustor branch rather than a plain premixed or nonpremixed branch
- inspect reverse-flow and return-state treatment at combustor exits or recirculating boundaries
- inspect whether flame-holding structure is being assumed rather than built coherently from pilot, recirculation, and backflow framing
- verify pilot and main-stream temperature, composition, and pressure framing together
- compare flameholder and recirculation-region setup against the nearest premixed tutorial lineage before widening the model family

deeper_checks:
- inspect whether the first instability forms in the recirculation bubble or flameholder region rather than across the full chamber
- separate return-state mismatch from a deeper premixed-field, thermo, or mesh hotspot problem
- only after the return state is coherent, compare startup controls against a safer staged baseline

likely_fixes:
- make flame-holding and returning mixture state explicit where reverse flow can occur
- rebuild pilot and main-stream structure from the nearest coherent baseline
- if the branch is actually plain premixed or diffusion-flame, leave this node and route accordingly

escalation_path:
- if the dominant issue is generic reverse-flow semantics, route to `outlet-backflow-role-confusion`
- if the real issue is a premixed ignition or flame-speed mismatch, route to `premixed-ignition-or-flame-speed-model-mismatch`
- if a local region is driving the failure, route to `critical-region-local-mesh-hotspot`

source_refs:
- official-openfoam-xifoam-guide
- official-openfoam-tutorial-premixed-combustion-xifoam
- official-openfoam-docs-inletOutlet-backflow
- community-simscale-docs-pressure-outlet-backflow

confidence: medium
notes:
- This node exists because recirculating combustors add a flame-holding and backflow branch that the plain premixed baseline does not capture cleanly.
