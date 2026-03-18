# Troubleshooting Node — Patch Name / Boundary Mismatch

id: patch-name-boundary-mismatch
symptom: The case errors early, ignores intended BC behavior, or shows obvious setup inconsistency because field-file patch entries do not align with the mesh boundary definition.

probable_causes:
- patch names in `boundaryField` do not match mesh boundary patch names
- field files copied from another case without patch renaming
- patch semantics changed in the mesh but not in the field dictionaries
- missing patch entries for one or more active fields

first_checks:
- inspect mesh boundary patch names
- compare patch names across all active field files under `0/`
- verify every active field contains the needed patch entries
- confirm patch physical roles were not silently changed during mesh edits

deeper_checks:
- compare with the nearest official tutorial structure for the same case family
- inspect whether the mismatch is limited to one field or systemic across turbulence/thermal/species fields too

likely_fixes:
- rename field patch entries to match the mesh
- add missing patch entries for all active fields
- rebuild BC review patch-by-patch after mesh edits

escalation_path:
- if patch names are correct but the case still behaves incorrectly, branch into BC semantics or solver-family mismatch rather than continuing name-only debugging

source_refs:
- community-simscale-kb-inconsistent-patch-patchfield
- official-openfoam-user-guide-case-structure
- official-openfoam-field-file-format
- official-openfoam-user-guide-boundary-conditions

confidence: high
notes:
- This is a structural setup failure class and should be checked before numerics tuning.
