# Distilled Rule — Localize Divergence Before Global Tuning

id: distilled-divergence-hotspot-localization-rule
kind: troubleshooting-rule

rule:
When a run diverges, first identify where the first unphysical quantity spikes; inspect nearby boundaries and local mesh quality before recommending broad global numerics changes.

why_it_matters:
- many "generic divergence" events are actually localized structural or mesh-quality failures
- global relaxation or timestep changes can hide, but not fix, a bad local region
- routing by hotspot location narrows the next troubleshooting branch much faster

recommended_agent_behavior:
- ask which field diverged first
- look for reported coordinates or reconstruct a hotspot from field data / post-processing
- review neighboring BC definitions and local mesh quality together
- only then escalate to global numerics stabilization advice

source_refs:
- community-simscale-kb-divergence-localization
- official-openfoam-user-guide-checkMesh
- official-openfoam-user-guide-boundary-conditions
- official-openfoam-mesh-quality-guidance

trust_note:
This rule blends medium-trust community workflow guidance with official mesh/boundary references; keep local mesh thresholds heuristic rather than absolute.
