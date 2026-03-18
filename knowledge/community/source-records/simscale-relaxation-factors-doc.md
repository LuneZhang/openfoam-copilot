# Source Record — SimScale Docs: Relaxation Factors

id: community-simscale-docs-relaxation-factors
source_type: community
source_name: SimScale Documentation
url: https://www.simscale.com/docs/simulation-setup/numerics/relaxation-factors/
date: unknown
trust_level: medium
tags:
- community
- numerics
- relaxation-factors
- convergence
- steady-state
solver_scope:
- steady-state
- general
physics_scope:
- general

summary: Vendor documentation page explaining under-relaxation as a stability-control mechanism and giving bounded practical ranges for manual startup tuning.

key_points:
- Relaxation factors are presented as a stability-versus-speed tradeoff rather than a universal cure.
- Values below roughly 0.15 are flagged as usually too slow to be practical.
- Values above roughly 0.7 are described as increasingly unstable, and above 0.9 as divergence-prone.
- A manual range around 0.3 to 0.7 is recommended when auto-relaxation does not behave well.
- The guidance is most relevant to steady-state startup, where first iterations are fragile.

applicability:
- conservative steady-state startup tuning
- documenting why relaxation-factor changes should come after structure, BC, and mesh checks
- building a troubleshooting node for overaggressive numerics

caveats:
- These are vendor heuristics, not official OpenFOAM limits.
- Exact safe ranges remain solver- and case-dependent.
- Using lower relaxation may hide structural setup mistakes instead of fixing them.
