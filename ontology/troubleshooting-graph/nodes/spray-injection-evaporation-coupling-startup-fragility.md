# Troubleshooting Node — Spray Injection, Evaporation, or Coupling Startup Fragility

id: spray-injection-evaporation-coupling-startup-fragility
symptom: A spray combustion case destabilizes at or near injection onset because parcel injection, evaporation coupling, and carrier-phase startup structure are inconsistent or too fragile.

probable_causes:
- injection timing or parcel properties are structurally mismatched to the carrier-phase reacting branch
- parcel temperature, diameter, or evaporation state is inconsistent with the intended injector setup
- a generic reacting template was reused without the spray-specific parcel layer
- generic reacting stiffness is being blamed before injection structure is coherent

first_checks:
- confirm the case really belongs to a spray branch rather than a plain reacting or premixed branch
- inspect injector timing, parcel properties, evaporation behavior, and carrier-phase reference state together
- compare injection dictionaries against the nearest official sprayFoam tutorial lineage before editing breakup or combustion detail
- inspect whether the first instability begins exactly at injection onset

deeper_checks:
- separate parcel and injector mismatch from a deeper thermo package or local hotspot problem
- inspect whether instability stays near the injector path rather than filling the whole domain immediately
- only after the spray structure is coherent, compare startup controls against a conservative transient spray baseline

likely_fixes:
- rebuild parcel, injector, and evaporation-coupling structure from the nearest spray tutorial baseline
- correct carrier-phase thermo reference state before later submodel tuning
- keep the branch transient and conservative across injection onset until startup is coherent

escalation_path:
- if the main issue is generic reacting stiffness after the parcel layer is coherent, route to `reacting-startup-coupling-too-stiff`
- if thermo is inconsistent, route to `thermo-chemistry-package-inconsistency`
- if a local region is driving the failure, route to `critical-region-local-mesh-hotspot`

source_refs:
- official-openfoam-sprayfoam-guide
- official-openfoam-tutorial-spray-combustion-sprayfoam
- official-openfoam-thermophysical-properties
- official-openfoam-user-guide-controlDict
- community-cfd-online-sprayfoam-startup-thread

confidence: medium
notes:
- This node exists because sprayFoam-style injection onset and evaporation coupling are a distinct first-check order, not just a generic reacting startup problem.
