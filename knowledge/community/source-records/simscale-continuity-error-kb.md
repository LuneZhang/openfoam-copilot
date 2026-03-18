# Source Record — SimScale KB: Continuity Error Encountered Cannot be Removed

id: community-simscale-kb-continuity-error
source_type: community
source_name: SimScale Knowledge Base
url: https://www.simscale.com/knowledge-base/continuity-error-encountered-cannot-be-removed/
date: 2021-01-26
trust_level: medium
tags:
- community
- troubleshooting
- continuity
- mass-balance
- pressure-reference
- boundary-conditions
solver_scope:
- general
- incompressible
- steady-state
- transient
physics_scope:
- general

summary: Vendor knowledge-base note framing the “continuity error cannot be removed” failure as a boundary-condition / global mass-balance problem, with explicit emphasis on pressure-outlet anchoring or another fixed-pressure reference.

key_points:
- The article treats non-removable continuity error as a symptom of inconsistent inlet/outlet boundary conditions rather than a standalone numerical defect.
- A primary failure mode is mismatch between inlet and outlet mass/volumetric flow treatment, so velocity and pressure BCs must be reviewed together.
- The note recommends a standard pair of velocity inlet plus pressure outlet for many practical flow cases.
- For custom BCs, it explicitly recommends `fixedValue` velocity with `zeroGradient` pressure on the inlet side, and `fixedValue` pressure with `zeroGradient` velocity on the outlet side.
- The article also states that ensuring any fixed pressure boundary condition can remove the continuity ambiguity, making pressure anchoring / reference treatment part of first-line triage.

applicability:
- triaging continuity-error crashes or persistent continuity warnings in open-domain flow setups
- distinguishing pressure-reference / BC-balance mistakes from generic solver-instability narratives
- routing agents to inspect pressure anchoring before broad relaxation-factor or timestep sweeps

caveats:
- The wording is broad and oriented toward common inlet/outlet flow setups, so closed cavities and buoyant branches still require solver-family-specific pressure treatment.
- The article is community/vendor guidance and should be combined with official solver-family documentation for `p` vs `p_rgh` or buoyancy-specific pressure handling.
- It is most useful as a routing signal for BC consistency and pressure anchoring, not as a universal prescription for every domain topology.
