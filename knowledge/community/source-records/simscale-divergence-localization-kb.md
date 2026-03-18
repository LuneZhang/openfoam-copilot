# Source Record — SimScale KB: How to Locate Divergence in Simulation?

id: community-simscale-kb-divergence-localization
source_type: community
source_name: SimScale Knowledge Base
url: https://www.simscale.com/knowledge-base/divergence-simulation-knowledge-base/
date: 2025-04-09
trust_level: medium
tags:
- community
- troubleshooting
- divergence
- localization
- mesh-quality
- postprocessing
solver_scope:
- general
- incompressible
- compressible
- thermal
- multiphase
physics_scope:
- general
- thermal
- multiphase

summary: Vendor knowledge-base article focused on locating where a CFD solution first diverges, using reported coordinates when available and post-processing plus mesh-quality inspection when coordinates are absent.

key_points:
- Divergence should be localized spatially before broad numerics tuning, because the first unstable region often reveals whether the failure is boundary-condition-driven or mesh-quality-driven.
- If the solver reports coordinates for the diverged quantity, first inspect that region and especially nearby boundaries for BC mistakes.
- If no coordinates are reported, use field post-processing (for example an iso-volume on the diverged variable) to identify the concentrated hotspot.
- Once the hotspot is found, inspect local mesh quality rather than assuming the whole domain is bad; even a small cluster of highly non-orthogonal or otherwise poor cells can trigger failure.
- Recommended remediation branches are local CAD cleanup, local refinement / meshing changes, and boundary-condition review near the hotspot.

applicability:
- early routing for runs that stop with divergence but without an obvious global setup error
- separating local structural/mesh failures from globally overaggressive numerics
- guiding agent behavior to ask "where did divergence start?" before proposing many parameter changes

caveats:
- SimScale references platform-specific post-processing affordances, but the underlying workflow maps to OpenFOAM practice through log parsing, field inspection, and local mesh-quality review.
- Mesh-quality thresholds in the article are heuristic and should not be treated as universal pass/fail lines outside source context.
