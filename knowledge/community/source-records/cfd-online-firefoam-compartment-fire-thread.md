# Source Record — CFD Online OpenFOAM Forum: fireFoam compartment-fire troubleshooting

id: community-cfd-online-firefoam-compartment-fire-thread
source_type: community
source_name: CFD Online OpenFOAM Forum
url: https://www.cfd-online.com/Forums/openfoam/
date: unknown
trust_level: low
tags:
- community
- forum
- combustion
- fireFoam
- compartment-fire
- p_rgh
- ventilation
solver_scope:
- reacting
- combustion
- buoyant
physics_scope:
- combustion
- fire
- buoyancy
- thermal

summary: Low-trust community discussion family highlighting that compartment-fire failures often narrow first on opening state, ventilation layout, and modified-pressure framing rather than on broad reacting numerics.

key_points:
- Ventilation openings should be reviewed as possible return-state boundaries, not as one-way exhausts.
- Community troubleshooting often checks `p_rgh`, gravity, and ambient reference choices before later fire-model tuning.
- fireFoam cases that look like generic instability can be structurally wrong at the room-opening level.

applicability:
- narrowing buoyant fire and compartment-fire startup failures
- deciding whether ventilation and reference-state review should come before wider reacting diagnosis

caveats:
- This is low-trust forum evidence and should only sharpen branch order after official anchors are loaded.
- The stored URL is a section-level pointer for the OpenFOAM forum surface, not a versioned fireFoam reference.
