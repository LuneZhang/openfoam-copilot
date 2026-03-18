# Troubleshooting Node — Buoyant Pressure Anchor / Reference-Height Mismatch

id: buoyant-pressure-anchor-reference-mismatch
symptom: A buoyant or gravity-influenced case already uses the expected modified-pressure branch (`p_rgh` or equivalent) but still shows unphysical pressure behavior, opening-boundary instability, or continuity failure that looks tied to pressure anchoring.

probable_causes:
- the solver family and `p_rgh` convention are nominally correct, but the reference-pressure / reference-height treatment is physically misplaced
- a fixed-pressure anchor is applied on the wrong patch, wrong pressure representation, or with the wrong hydrostatic interpretation
- buoyant openings are treated like generic incompressible outlets without respecting modified-pressure semantics
- gravity direction, reference height, and opening location are inconsistent with the intended hydrostatic framing
- the case mixes static-pressure intuition with modified-pressure boundary logic copied from another branch

first_checks:
- confirm the case is not a plain `p` versus `p_rgh` mistake; only stay on this node if the modified-pressure branch itself is already correct
- inspect where the effective pressure anchor actually lives: patch BC, reference height, or solver-side reference treatment
- verify gravity direction, reference height, and opening elevation are physically coherent for the geometry
- check whether the boundary treatment assumes generic outlet behavior when the buoyant branch really needs modified-pressure-aware pressure handling
- compare the pressure-anchor pattern against the nearest official buoyant tutorial family rather than against a non-buoyant open-domain template

deeper_checks:
- inspect whether continuity failure appears immediately, which suggests structural anchoring error rather than later numerics drift
- separate wrong reference-height / hydrostatic interpretation from wrong thermal BC pairing at the same opening
- check whether the selected anchor location makes sense for a domain with multiple openings or mixed inflow/outflow behavior
- verify that turbulence or temperature companion fields are not making the opening behavior look like a pressure problem when the anchor itself is actually fine

likely_fixes:
- move or redefine the pressure anchor so it matches the intended buoyant opening logic and geometry
- replace generic outlet-pressure intuition with buoyant-branch-specific modified-pressure treatment
- correct reference height / hydrostatic framing so pressure level and opening behavior are physically interpretable
- rebuild opening BCs as a coupled `U` / `p_rgh` / `T` set instead of patching only one field in isolation

escalation_path:
- if the wrong pressure variable is being solved entirely, route back to `p-vs-p_rgh-confusion`
- if the issue is a generic open-domain BC balance problem rather than hydrostatic framing, route to `unremovable-continuity-error-bc-balance`
- if pressure anchoring is coherent but instability still grows later, route to `courant-driven-transient-instability`, `continuity-error-growth`, or mesh-localized diagnosis

source_refs:
- official-openfoam-hydrostatic-pressure-effects
- community-simscale-docs-modified-pressure-reference
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-user-guide-controlDict

confidence: medium
notes:
- This node exists to separate “wrong pressure variable” from “right variable, wrong hydrostatic anchor semantics.”
- In buoyant cases, pressure anchoring can be structurally wrong even when the field name itself is correct.
