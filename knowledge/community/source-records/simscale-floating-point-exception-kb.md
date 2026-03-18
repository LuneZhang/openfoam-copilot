# Source Record — SimScale KB: Floating Point Exception

id: community-simscale-kb-floating-point-exception
source_type: community
source_name: SimScale Knowledge Base
url: https://www.simscale.com/knowledge-base/floating-point-exception/
date: 2022-09-09
trust_level: medium
tags:
- community
- troubleshooting
- floating-point-exception
- divergence
- timestep
- boundary-conditions
solver_scope:
- general
- compressible
- incompressible
- multiphase
physics_scope:
- general
- thermal
- multiphase

summary: Vendor knowledge-base article summarizing common floating-point-exception triggers and first-line remedies across several CFD analysis classes.

key_points:
- Floating point exception is framed as a division-by-zero or numerical blow-up symptom rather than a root cause by itself.
- For compressible and convective-heat-transfer branches, zero pressure or missing reference-pressure treatment is highlighted as a common trigger.
- For other branches, zero turbulence quantities or other nonphysical initial/boundary values are called out as typical startup killers.
- Large timestep / Courant control is identified as a major instability lever, especially for multiphase and dynamic cases.
- Upwind or bounded-upwind convection is recommended as a conservative fallback when higher-order schemes destabilize startup.

applicability:
- early triage of floating-point-exception crashes
- ordering first checks before blind relaxation-factor tweaking
- building bounded troubleshooting nodes for startup divergence

caveats:
- SimScale terminology maps onto OpenFOAM concepts but not always one-to-one with raw dictionary names.
- Advice is intentionally broad; it should not override solver-family-specific official guidance.
- Recommended numerics fallback is stability-first, not accuracy-optimal.
