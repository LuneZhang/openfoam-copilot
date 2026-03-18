# Source Record — SimScale Docs: Non-Orthogonal Correctors

id: community-simscale-docs-non-orthogonal-correctors
source_type: community
source_name: SimScale Documentation
url: https://www.simscale.com/docs/simulation-setup/numerics/non-orthogonal-correctors/
date: unknown
trust_level: medium
tags:
- community
- mesh
- non-orthogonality
- numerics
- pressure-correction
solver_scope:
- general
- incompressible
- compressible
- steady-state
- transient
physics_scope:
- general

summary: Vendor numerics documentation explaining that higher mesh non-orthogonality degrades pressure calculation and may require extra correction loops, making localized bad-cell regions especially relevant even when the mesh is globally usable.

key_points:
- For modest non-orthogonality, standard pressure-coupling treatment may remain adequate.
- For bad-quality meshes, additional correction is needed because pressure calculation becomes more fragile.
- The guidance links mesh non-orthogonality directly to pressure-iteration burden rather than treating it as a cosmetic warning.
- This supports the idea that a limited region of highly non-orthogonal cells can dominate failure behavior if it sits in a pressure-sensitive hotspot.

applicability:
- diagnosing cases where pressure-related instability persists despite acceptable global mesh statistics
- interpreting whether local non-orthogonality is likely to be numerically consequential
- supporting a node for critical-region local mesh hotspots and pressure-sensitive failure regions

caveats:
- Thresholds are heuristic, not canonical OpenFOAM limits.
- Extra correction loops can stabilize a marginal mesh temporarily but do not erase a structurally bad local region.
- The page is best used as bounded numerics context, not as permission to ignore bad cells.
