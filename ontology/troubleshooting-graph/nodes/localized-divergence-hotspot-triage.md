# Troubleshooting Node — Localized Divergence Hotspot Triage

id: localized-divergence-hotspot-triage
symptom: The run diverges or crashes, and logs or field inspection indicate one localized region where an unphysical quantity first spikes.

probable_causes:
- boundary-condition mistake near the divergence hotspot
- locally poor mesh quality or tiny CAD features creating bad cells
- a physically sharp region that needs better local resolution or gentler startup
- a real local instability being masked as a generic global divergence message

first_checks:
- determine which field diverged first and whether coordinates or a local hotspot can be identified
- inspect boundaries adjacent to the hotspot before changing global numerics
- inspect local mesh quality near the hotspot instead of only domain-wide summary metrics
- check whether the hotspot aligns with a known geometric small feature, gap, or abrupt topology transition

deeper_checks:
- compare the hotspot with local non-orthogonality, skewness, and aspect-ratio issues
- inspect whether the same region also shows patch typing mistakes, `empty` misuse, or solver-family inconsistency
- distinguish a truly local defect from a globally fragile case that only first manifests there

likely_fixes:
- correct BC assignments near the hotspot
- clean or simplify CAD features causing locally bad cells
- add local mesh refinement or improve meshing controls in that region
- restart with a gentler initialization only after structural and local-quality checks are done

escalation_path:
- if no meaningful hotspot can be isolated, branch into broader numerics / solver-stability diagnosis rather than overfitting to one region
- if the hotspot maps cleanly to a specific patch or mesh defect, route into the more specific structural node for that failure class

source_refs:
- community-simscale-kb-divergence-localization
- official-openfoam-user-guide-checkMesh
- official-openfoam-mesh-quality-guidance
- official-openfoam-user-guide-boundary-conditions

confidence: medium
notes:
- Prefer localizing the first divergence region before spending time on global relaxation-factor sweeps.
