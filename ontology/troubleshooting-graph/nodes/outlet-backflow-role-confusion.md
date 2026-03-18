# Troubleshooting Node — Outlet Backflow / Inlet-Outlet Role Confusion

id: outlet-backflow-role-confusion
symptom: The run destabilizes near an outlet patch, shows persistent reverse flow or unphysical recirculation at the boundary, or behaves as if an outlet patch is intermittently acting like an inlet.

probable_causes:
- a nominal outlet patch is seeing sustained reverse flow but is configured with an outflow-only assumption
- the selected outlet BC does not provide physically meaningful inflow/backflow values when recirculation reaches the boundary
- the outlet is placed too close to a recirculating region, wake, buoyant return path, or separated flow structure
- pressure / velocity outlet logic is structurally mismatched for the actual flow direction behavior
- thermal or turbulence companion fields are under-specified during backflow even if `U` / pressure entries look reasonable

first_checks:
- inspect the sign and persistence of flux at the outlet patch instead of assuming it is a pure outflow boundary
- verify whether the selected outlet treatment can handle reverse flow and whether its backflow-side values are physically meaningful
- check whether outlet recirculation is an expected feature of the geometry or a sign that the boundary is placed too close to the active flow region
- review pressure / velocity pairing on the inlet and outlet boundaries as a coupled system, not field-by-field
- if thermal or turbulent transport is active, verify that backflow-relevant temperature and turbulence quantities are not left physically undefined

deeper_checks:
- compare the current outlet treatment against the closest official tutorial family for the same solver branch
- inspect whether instability localizes at the outlet first or only appears there after upstream divergence has already started
- test whether extending the outlet region or simplifying startup conditions removes the reverse-flow-triggered instability
- separate true outlet-role confusion from pressure-anchoring mistakes and from mesh-localized recirculation hotspots

likely_fixes:
- switch from an outflow-only assumption to a reverse-flow-tolerant outlet treatment where appropriate
- provide physically plausible backflow values for transported quantities instead of leaving the return state implicit
- move the outlet boundary farther from wakes, separation zones, or buoyant recirculation regions
- correct complementary pressure / velocity BC pairing so the boundary is not structurally over- or under-constrained
- if backflow is merely a symptom, route next into pressure-anchor, mesh-hotspot, or global instability diagnosis rather than endlessly retuning numerics

escalation_path:
- if reverse flow is real and persistent, branch into solver-family-specific outlet treatment and pressure-anchoring review
- if the outlet only appears problematic because divergence starts upstream, branch into localized-divergence, mesh-quality, or Courant-driven instability instead
- if the failure appears only after decomposition, branch into the parallel-only failure path rather than treating it as a purely local outlet issue

source_refs:
- official-openfoam-docs-inletOutlet-backflow
- community-simscale-docs-pressure-outlet-backflow
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-field-file-format

confidence: medium
notes:
- This node is for cases where the boundary-condition role is structurally wrong or physically incomplete, not for all recirculation.
- Reverse flow at an outlet is a routing clue, not automatically proof that numerics are the root cause.
