# Troubleshooting Node — Courant-Driven Transient Instability

id: courant-driven-transient-instability
symptom: A transient case becomes unstable as Courant number grows, often after an initially acceptable startup phase.

probable_causes:
- timestep too large for evolving local flow speeds
- weak `adjustTimeStep` / `maxCo` control
- aggressive transient startup in a strongly coupled case
- mesh quality or local cell size making local CFL conditions much worse than expected

first_checks:
- inspect `deltaT`, `adjustTimeStep`, and `maxCo` in `controlDict`
- identify whether instability begins only after local velocity or interface growth
- compare global and local stability expectations, especially in fine or poor-quality regions
- review whether startup numerics are too aggressive for the transient phase

deeper_checks:
- inspect whether mesh quality or local resolution is amplifying the effective Courant restriction
- compare against the nearest official transient tutorial family for runtime-control style
- inspect whether the case should start from a more conservative transient ramp-up

likely_fixes:
- reduce timestep and tighten Courant control
- enable or refine adaptive timestep management
- use more conservative startup numerics until the transient structure stabilizes
- repair mesh hotspots that force impractically small local stability limits

escalation_path:
- if Courant control is tightened and the case still fails, branch into mesh-quality-driven-instability or thermo/multiphase-specific startup problems

source_refs:
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- community-simscale-kb-floating-point-exception

confidence: high
notes:
- Courant number is a runtime-control symptom channel, not a full diagnosis by itself.
