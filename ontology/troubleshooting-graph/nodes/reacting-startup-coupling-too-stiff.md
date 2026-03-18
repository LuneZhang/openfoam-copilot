# Troubleshooting Node — Reacting Startup Coupling Too Stiff

id: reacting-startup-coupling-too-stiff
symptom: A reacting or combustion case looks structurally plausible on first review, but startup still blows up or behaves violently because thermo, species, and source-term coupling are too stiff for the current launch path.

probable_causes:
- the case is being pushed into an aggressive startup before thermo, species, and flow fields have formed a stable coupled baseline
- startup numerics are too ambitious for the current reacting source terms and scalar gradients
- a staged or transient startup path is needed before attempting the intended target workflow
- local heat-release or scalar-gradient hotspots make the startup much stiffer than the global case framing suggests
- the solver family is nominally plausible, but the startup path is still too aggressive for the current field state

first_checks:
- confirm solver family, thermo package, chemistry model, and required species fields are structurally coherent before blaming startup stiffness alone
- inspect whether the run destabilizes before meaningful chemistry/transport evolution has settled, which suggests startup stiffness rather than later physical-model failure
- review thermal, species, and pressure-related BCs as one reacting system rather than adjusting one field in isolation
- inspect whether a small hotspot region is creating the first instability, rather than the whole case being globally impossible
- compare the current launch path against a more conservative staged or transient reacting tutorial lineage for the same problem family

deeper_checks:
- compare current `controlDict`, `fvSchemes`, and `fvSolution` against a conservative reacting startup baseline rather than a mature target-state setup
- separate true reacting startup stiffness from cases where solver family or thermo/chemistry structure is actually wrong
- verify that the mesh is locally robust in flame-front / scalar-gradient regions before assuming chemistry stiffness is the only culprit
- inspect whether turbulence/combustion coupling is being activated too early relative to the structural certainty of the case

likely_fixes:
- use a staged or transient startup path to establish a stable thermo/species baseline before pushing the intended target solve
- lower startup aggressiveness in timestep and numerical controls before retrying
- keep the final target workflow if needed, but only after the coupled reacting fields settle through a safer startup phase
- if structural issues remain, fix thermo, chemistry, BC, or hotspot problems before retrying the startup path

escalation_path:
- if solver family or thermo/chemistry structure is actually wrong, route to `wrong-solver-family-selection` or `thermo-chemistry-package-inconsistency`
- if the real issue is a local hotspot, route to `critical-region-local-mesh-hotspot`
- if the run remains unstable even under conservative staged/transient startup, route into wider reacting BC / mesh / turbulence diagnosis rather than insisting on the original launch path

source_refs:
- official-openfoam-user-guide-solver-selection
- official-openfoam-thermophysical-properties
- official-openfoam-compressible-setup-guidance
- official-openfoam-user-guide-controlDict
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution
- community-simscale-docs-relaxation-factors
- community-simscale-kb-floating-point-exception

confidence: medium
notes:
- This node is not for every difficult combustion case.
- It is for cases where the structural setup may be broadly correct, but the chosen startup path is too stiff for the initial coupled state.
