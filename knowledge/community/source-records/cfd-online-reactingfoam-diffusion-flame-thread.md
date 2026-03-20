# Source Record — CFD Online OpenFOAM Forum: reactingFoam diffusion-flame troubleshooting

id: community-cfd-online-reactingfoam-diffusion-flame-thread
source_type: community
source_name: CFD Online OpenFOAM Forum
url: https://www.cfd-online.com/Forums/openfoam/
date: unknown
trust_level: low
tags:
- community
- forum
- combustion
- reactingFoam
- diffusion-flame
- species
- backflow
solver_scope:
- reacting
- combustion
- nonpremixed
physics_scope:
- combustion
- reacting
- thermal

summary: Low-trust community discussion family highlighting that diffusion-flame failures often trace back to stream composition definition, species boundary coherence, and reverse-flow state treatment before they become pure chemistry-stiffness problems.

key_points:
- Separated fuel and oxidizer streams should be reviewed as a coupled structural definition, not as independent inlet tweaks.
- Reverse-flow regions can feed undefined species states back into the domain if outlet treatment is copied from a non-reacting case.
- Community practitioners repeatedly compare diffusion-flame setups against a known tutorial lineage before changing chemistry detail.

applicability:
- narrowing nonpremixed or diffusion-flame startup failures
- deciding whether a reactingFoam case is structurally wrong before broader numerics retuning

caveats:
- This is low-trust forum evidence and should not replace official solver or tutorial anchors.
- The stored URL is a section-level pointer for the OpenFOAM forum surface, not a canonical solver manual.
