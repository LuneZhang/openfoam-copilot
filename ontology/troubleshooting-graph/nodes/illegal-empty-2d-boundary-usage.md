# Troubleshooting Node — Illegal Empty 2D Boundary Usage

id: illegal-empty-2d-boundary-usage
symptom: The case fails during setup or very early execution with an error about illegal `empty` usage, inconsistent boundary-condition types, or a pseudo-2D case that is not actually one-cell thick.

probable_causes:
- `empty` was assigned on a mesh that is actually 3D
- the mesh is intended to be pseudo-2D but has more than one cell in the thin direction
- the pseudo-2D faces normal to the thin direction were not all assigned `empty`
- a copied tutorial field set preserved `empty` on the wrong patches after geometry changes

first_checks:
- inspect the thin direction and count cells through that direction
- check which faces are normal to the pseudo-2D thickness direction
- verify `empty` appears only on the out-of-plane faces of a one-cell-thick mesh
- confirm the rest of the boundary conditions are 3D-compatible if the case is not pseudo-2D

deeper_checks:
- compare the mesh and `0/` field files against the nearest official pseudo-2D tutorial pattern
- inspect `constant/polyMesh/boundary` to confirm patch typing aligns with the intended dimensionality
- check whether the case should really be modeled as 3D with symmetry instead of forcing `empty`

likely_fixes:
- remove `empty` from ordinary 3D patches and replace with physically valid 3D BCs
- rebuild the mesh as a true one-cell-thick pseudo-2D mesh if `empty` is required
- assign `empty` consistently to all out-of-plane faces only
- re-run structural BC review before touching numerics

escalation_path:
- if `empty` usage is corrected but startup still fails, branch into patch-type / patchField inconsistency or broader BC semantics review

source_refs:
- community-simscale-kb-empty-2d-boundary
- community-simscale-kb-inconsistent-patch-patchfield
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-field-file-format

confidence: medium
notes:
- This is a structural admissibility problem; numerics tuning should wait until dimensionality and patch typing are coherent.
