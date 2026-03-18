# Source Record — SimScale Docs: Modified Pressure / Hydrostatic Reference Height

id: community-simscale-docs-modified-pressure-reference
source_type: community
source_name: SimScale Documentation
url: https://www.simscale.com/docs/simulation-setup/boundary-conditions/pressure-inlet-and-pressure-outlet/
date: unknown
trust_level: medium
tags:
- community
- boundary-conditions
- p_rgh
- modified-pressure
- hydrostatic-pressure
- reference-height
- buoyancy
solver_scope:
- buoyant
- compressible
- thermal
- multiphase
physics_scope:
- thermal
- buoyancy
- compressible

summary: Vendor documentation page explaining modified pressure (`p_rgh`) and hydrostatic pressure handling, including the role of reference height in pressure boundary definitions when buoyancy effects matter.

key_points:
- Modified pressure is explicitly framed as `p_rgh = p - rho g h` for buoyancy-sensitive analyses.
- Hydrostatic pressure options require a reference height rather than an arbitrary scalar outlet-pressure interpretation.
- The reference height is the location where hydrostatic pressure equals static pressure, which means anchor placement has physical meaning.
- A buoyant case can therefore be structurally wrong even when it already uses `p_rgh`, if the reference-pressure / reference-height treatment is inconsistent with geometry and gravity.

applicability:
- diagnosing buoyant cases that already use `p_rgh` but still show unphysical pressure anchoring or opening behavior
- distinguishing wrong pressure-variable choice from wrong modified-pressure anchoring
- reviewing hydrostatic outlet / opening setup in buoyant and thermo-coupled cases

caveats:
- SimScale terminology maps onto OpenFOAM concepts but may not match raw dictionary names exactly.
- This is vendor documentation, not a substitute for solver-family-specific official pressure-boundary guidance.
- Correct anchor placement still depends on geometry, gravity direction, and chosen solver branch.
