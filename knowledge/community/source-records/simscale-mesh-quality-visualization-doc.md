# Source Record — SimScale Docs: Mesh Quality Visualization Tips

id: community-simscale-docs-mesh-quality-visualization
source_type: community
source_name: SimScale Documentation
url: https://www.simscale.com/docs/simulation-setup/meshing/mesh-quality/
date: unknown
trust_level: medium
tags:
- community
- mesh
- mesh-quality
- non-orthogonality
- skewness
- visualization
solver_scope:
- general
- incompressible
- compressible
- thermal
physics_scope:
- general

summary: Vendor documentation defining key mesh-quality measures such as non-orthogonality and skewness and emphasizing inspection of problematic cell-quality distributions rather than only headline pass/fail status.

key_points:
- Non-orthogonality is explicitly framed on a 0-to-90 scale from ideal to worst.
- Skewness is defined as a geometric distortion measure tied to interpolation accuracy degradation.
- The material is useful for identifying which quality metric is locally dominant instead of treating all mesh warnings as equivalent.
- A numerically dangerous mesh can therefore be hidden inside an otherwise acceptable overall mesh summary if the bad cells cluster in sensitive regions.

applicability:
- reviewing local mesh-quality hotspots after global `checkMesh` looks manageable
- distinguishing non-orthogonality-driven pressure sensitivity from other local mesh defects
- supporting a troubleshooting node for critical-region local mesh hotspots

caveats:
- This is vendor guidance, not an OpenFOAM-specific convergence guarantee.
- Threshold usefulness still depends on solver family, discretization, and local physics.
- The article is strongest as a triage aid, not as a universal accept/reject policy.
