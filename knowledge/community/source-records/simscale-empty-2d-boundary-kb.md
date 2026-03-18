# Source Record — SimScale KB: Incorrect Usage of Empty 2D Boundary Condition

id: community-simscale-kb-empty-2d-boundary
source_type: community
source_name: SimScale Knowledge Base
url: https://www.simscale.com/knowledge-base/incorrect-usage-of-empty-2d-boundary-condition/
date: 2020-12-15
trust_level: medium
tags:
- community
- troubleshooting
- boundary-conditions
- empty
- 2d
- pseudo-2d
solver_scope:
- general
- incompressible
- compressible
- multiphase
physics_scope:
- general
- multiphase
- thermal

summary: Vendor knowledge-base article explaining that `empty` can only be used for pseudo-2D OpenFOAM meshes that are exactly one cell thick in the out-of-plane direction, and otherwise becomes a structural BC-type error.

key_points:
- `empty` is only valid when the mesh is truly pseudo-2D in the OpenFOAM sense, with exactly one cell through the thin direction.
- A common failure mode is applying `empty` to a normal 3D mesh because the user conceptually wants a 2D problem.
- A second failure mode is having a pseudo-2D mesh but failing to assign the `empty` condition to the faces normal to the one-cell-thick direction.
- The article recommends switching back to standard 3D-compatible BCs (for 3D cases) or rebuilding the mesh as one-cell-thick and assigning `empty` consistently (for pseudo-2D cases).

applicability:
- triaging startup errors about illegal `empty` usage or inconsistent BC types
- case review for 2D/pseudo-2D imported OpenFOAM meshes
- routing setup reviews away from numerics changes when the real issue is dimensionality / patch typing

caveats:
- SimScale only supports 3D mesh uploads, so some platform phrasing is product-specific.
- The article is about admissibility of `empty`, not about whether a pseudo-2D approximation is physically appropriate for the target problem.
