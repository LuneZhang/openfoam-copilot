# Tutorial Pattern Extraction Seeds

id: tutorial-pattern-extraction-seeds-v1
problem_class: setup
confidence: high
source_refs:
- official-openfoam-tutorial-conventions
- official-openfoam-tutorial-catalog

## Why this note exists

Phase 1 does not need full tutorial transcription. What it needs first is a stable extraction frame so future tutorial harvesting stays comparable across solver families. These seeds define the minimum pattern classes worth extracting from official tutorials before collecting case-by-case details.

## Extraction principle

Do not ask: "What files are in this tutorial?"
Ask instead:
1. what problem class does this tutorial represent?
2. why does the chosen solver family fit that problem?
3. which dictionaries and fields are essential rather than incidental?
4. what startup/stability patterns are reusable in nearby cases?
5. what parts are tutorial-specific and should not be overgeneralized?

## Seed pattern set

### Seed A — incompressible laminar baseline

Use for tutorials that teach the cleanest `U`/`p` workflow with minimal physics overhead.

Extract:
- solver family and steady/transient character
- minimum required fields under `0/`
- pressure/velocity BC pairing pattern
- mesh simplicity assumptions
- which numerics are conservative teaching defaults vs production-worthy choices

Reusable value:
- base case anatomy
- first-pass debugging order
- low-complexity template for agent bootstrapping

### Seed B — incompressible turbulent baseline

Use for tutorials that add RANS/LES fields on top of the incompressible structure.

Extract:
- turbulence model activation path
- added fields and `constant/` dictionaries
- wall-function or near-wall requirements
- whether numerics and initialization are visibly changed to handle turbulence

Reusable value:
- minimal delta from laminar to turbulent setup
- turbulence-specific field/BC checklist
- startup risk indicators introduced by turbulence closure

### Seed C — compressible / thermo baseline

Use for tutorials where energy and thermophysical coupling are core rather than optional.

Extract:
- pressure variable convention
- temperature/enthalpy-related fields
- `thermophysicalProperties` structure role
- gravity/buoyancy relevance where present
- extra observability needs beyond incompressible runs

Reusable value:
- distinction between incompressible intuition and thermo-coupled workflows
- required property-file audit items

### Seed D — heat-transfer / buoyant pattern

Use for tutorials where thermal boundary conditions and gravity are major drivers.

Extract:
- role of `T`, `p_rgh`, and `g` where applicable
- coupling between flow and temperature BCs
- stability controls related to thermal startup
- what makes the case a buoyant-flow template rather than generic thermal transport

Reusable value:
- agent guardrails for buoyancy-specific setup review
- first-pass BC audit for mixed thermal/flow problems

### Seed E — multiphase pattern

Use for tutorials with phase fraction fields and interface handling.

Extract:
- additional core fields
- interfacial model dependencies
- timestep/Courant constraints that appear stricter than single-phase cases
- which output diagnostics matter most during startup

Reusable value:
- warning that multiphase templates should not be treated as normal single-phase variants
- first-pass instability review points

### Seed F — reacting / combustion pattern

Use for tutorials involving chemistry, heat release, or species transport.

Extract:
- solver/model family boundary
- species/thermo dictionary expansion
- ignition/initialization sensitivity
- what tutorial assumptions are purely pedagogical

Reusable value:
- separation of combustion structure from generic thermal structure
- shortlist of files and fields agents must verify before runtime tuning

## Standard extraction fields for future notes

Every future tutorial-pattern note should answer at least:
- scenario name
- representative solver family
- steady vs transient intent
- required `0/` fields
- key `constant/` dictionaries
- key `system/` dictionaries
- initialization guidance
- stability risks
- debug priority order
- source refs

## Anti-patterns

- copying folder trees without identifying essential vs tutorial-specific content
- treating a tutorial’s numerics as universal best practice
- merging laminar, turbulent, thermal, and multiphase patterns into one generic template
- extracting file names while ignoring the problem statement the tutorial solves

## Recommendation

Use these six seed classes as the Phase 1 extraction queue. Fill one representative note per class before expanding into narrower subfamilies.

## Rationale

- Phase 1 needs reusable pattern coverage, not encyclopedic tutorial dumping.
- Solver-family templates become more reliable when extracted with the same frame.
- Later community troubleshooting notes will be easier to align if tutorial baselines already exist.

## Applicability limits

- Some official tutorials span multiple pattern classes.
- Fork/version differences may change specific file names or solver choices.
- Final templates still need scenario-specific trimming before agent use.
