# Source Record — SimScale Docs: k-omega SST Guidance

id: community-simscale-docs-k-omega-sst-guidance
source_type: community
source_name: SimScale Documentation
url: https://www.simscale.com/docs/simulation-setup/global-settings/k-omega-sst/
date: unknown
trust_level: medium
tags:
- community
- turbulence
- k-omega-sst
- rans
- wall-treatment
- free-stream-sensitivity
solver_scope:
- incompressible
- rans
- external-aero
- general
physics_scope:
- general

summary: Vendor turbulence-model guidance describing k-omega SST as a blend that leverages k-omega accuracy near walls and k-epsilon behavior in the free stream, while noting sensitivity to free-stream turbulence quantities.

key_points:
- The guidance explicitly contrasts near-wall and free-stream behavior between k-epsilon and k-omega families.
- k-omega-side behavior is presented as stronger near the wall, which makes wall-region field and patch treatment especially important.
- The documentation notes sensitivity to free-stream values of turbulence quantities, meaning inlet/opening turbulence fields can destabilize an otherwise plausible case.
- A startup problem may therefore come from turbulence-field family / patch-role mismatch rather than from pressure or numerics first.

applicability:
- diagnosing RANS startup cases where inlet/opening turbulence values or wall treatment look copied from the wrong model family
- distinguishing wall-sensitive turbulence setup failures from generic residual blow-up
- supporting a troubleshooting node for turbulence-field-family and patch-role inconsistency

caveats:
- This is vendor guidance, not a substitute for OpenFOAM model-specific official documentation.
- It should guide triage order rather than be treated as a hard performance guarantee.
- Mesh resolution and y-plus strategy still control whether the chosen wall treatment is appropriate.
