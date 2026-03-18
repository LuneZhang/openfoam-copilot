# Source Record — SimScale Docs: Pressure Inlet and Pressure Outlet (backflow handling)

id: community-simscale-docs-pressure-outlet-backflow
source_type: community
source_name: SimScale Documentation
url: https://www.simscale.com/docs/simulation-setup/boundary-conditions/pressure-inlet-and-pressure-outlet/
date: unknown
trust_level: medium
tags:
- community
- boundary-conditions
- pressure-outlet
- backflow
- recirculation
- thermal
solver_scope:
- incompressible
- compressible
- thermal
- general
physics_scope:
- general
- thermal
- compressible

summary: Vendor documentation page for pressure inlet / pressure outlet usage that explicitly treats outlet recirculation as a case where fluid can re-enter the domain and therefore needs physically meaningful backflow-side values.

key_points:
- Pressure-outlet treatment may need explicit backflow-side quantities when outlet recirculation occurs.
- In thermal/compressible framing, backflow temperature is not decorative metadata; it represents the state of fluid re-entering the domain.
- Outlet recirculation means a nominal outlet patch can temporarily behave like an inflow boundary for some transported quantities.
- A pressure-based outlet setup that ignores reverse-flow behavior can remain syntactically valid while still being physically under-specified.

applicability:
- diagnosing outlet-region instability or nonphysical recirculation near pressure outlets
- distinguishing BC-role confusion from generic numerics instability
- deciding when reverse-flow-tolerant outlet treatment is needed

caveats:
- SimScale terminology maps onto OpenFOAM concepts but may not match raw field-file names exactly.
- This is vendor documentation, not canonical OpenFOAM wording.
- The page is especially informative for thermal/compressible backflow semantics, not a full replacement for solver-family-specific setup review.
