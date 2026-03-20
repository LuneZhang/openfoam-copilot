# Source Record — CFD Online OpenFOAM Forum: sprayFoam startup troubleshooting

id: community-cfd-online-sprayfoam-startup-thread
source_type: community
source_name: CFD Online OpenFOAM Forum
url: https://www.cfd-online.com/Forums/openfoam/
date: unknown
trust_level: low
tags:
- community
- forum
- combustion
- sprayFoam
- spray
- injection
- parcels
solver_scope:
- reacting
- combustion
- spray
physics_scope:
- combustion
- spray
- thermal
- multiphase

summary: Low-trust community discussion family highlighting that sprayFoam failures often start at injection onset because parcel, injector, and carrier-phase startup definitions are structurally inconsistent.

key_points:
- Injector timing and parcel properties are treated as first-pass structural checks rather than minor submodel details.
- Practitioners often inspect whether instability begins exactly at injection onset.
- Carrier-phase thermo and parcel setup are repeatedly reviewed together before later breakup or combustion-model tuning.

applicability:
- narrowing spray-combustion startup failures
- deciding whether injector or parcel structure should be checked before generic reacting stiffness

caveats:
- This is low-trust forum evidence and should not override official sprayFoam anchors.
- The stored URL is a section-level pointer for the OpenFOAM forum surface, not a versioned solver reference.
