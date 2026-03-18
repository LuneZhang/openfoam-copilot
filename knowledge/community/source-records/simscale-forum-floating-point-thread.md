# Source Record — SimScale Forum: Most Popular Errors of Simulation (Floating Point Exception advice)

id: community-simscale-forum-floating-point-thread
source_type: community
source_name: SimScale Forum
url: https://www.simscale.com/forum/t/most-popular-errors-of-simulation/92/3
date: 2015-08-03
trust_level: low
tags:
- community
- forum
- floating-point-exception
- divergence
- heuristics
solver_scope:
- steady-state
- general
physics_scope:
- general

summary: Practitioner forum reply collecting personal heuristics for floating-point-exception crashes, including bounded-upwind fallback, nonzero physical initial values, and timestep reduction.

key_points:
- Floating point exception is described as a divergence symptom rather than a unique diagnosis.
- Bounded upwind is suggested as a stability-first fallback for steady-state startup.
- Zero or nonphysical values for temperature, pressure in compressible cases, or turbulence quantities are highlighted as common triggers.
- Large timestep is flagged as especially risky during first iterations and in VOF-like multiphase behavior.

applicability:
- low-confidence heuristic enrichment after official and higher-trust checks
- extracting symptom language from practitioner experience
- reinforcing conservative startup order in troubleshooting nodes

caveats:
- Explicitly personal experience, not authoritative guidance.
- Advice is broad and should be downgraded when solver family or physics branch is unclear.
- Best used as corroboration, not as a sole source.
