# Source Record — SimScale KB: Inconsistent Patch and PatchField Types Found

id: community-simscale-kb-inconsistent-patch-patchfield
source_type: community
source_name: SimScale Knowledge Base
url: https://www.simscale.com/knowledge-base/inconsistent-patch-and-patchfield-types-found/
date: 2019-09-30
trust_level: medium
tags:
- community
- troubleshooting
- boundary-conditions
- mesh
- patch-type
- patchfield
solver_scope:
- general
- incompressible
- compressible
- cht
physics_scope:
- general
- thermal

summary: Vendor knowledge-base article for a structural setup failure where mesh patch type in `constant/polyMesh/boundary` is inconsistent with the boundary-condition type applied in field files or GUI setup.

key_points:
- The error is framed as a mismatch between mesh-level `patch type` and field-level `patchField type`, not as a numerics instability.
- Typical trigger is importing or editing a mesh/case where boundary semantics changed but `0/` field assignments were not updated accordingly.
- The article gives a concrete example: a mesh patch marked `symmetry` cannot be assigned a generic `zeroGradient` field treatment.
- First-line remediation is to inspect `constant/polyMesh/boundary` and make each patch's field-side BC type consistent with the mesh-side patch classification.

applicability:
- early triage of startup errors that mention inconsistent patch / patchField types
- distinguishing structural BC/type mismatches from ordinary patch-name mistakes
- strengthening agent checks that compare mesh metadata against field dictionaries

caveats:
- SimScale wording is platform-oriented, but the underlying OpenFOAM concept maps directly to raw case-upload workflows.
- Article focuses on consistency, not on choosing the physically correct BC after consistency is restored.
