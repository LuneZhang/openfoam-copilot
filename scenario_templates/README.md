# Scenario Templates

Reusable scenario templates derived from Phase 1 official-tutorial patterns.

Current batch:
- `incompressible-laminar-internal-flow.md`
- `incompressible-rans-external-aerodynamics.md`
- `buoyant-natural-convection-room-scale.md`
- `compressible-thermo-flow-generic.md`
- `multiphase-interface-flow-generic.md`
- `reacting-combustion-flow-generic.md`
- `premixed-combustion-baseline.md`
- `nonpremixed-diffusion-flame.md`
- `buoyant-fire-compartment.md`
- `partially-premixed-recirculating-combustor.md`
- `spray-combustion.md`

Compatibility alias:
- `reacting-combustion-generic-template.md` (deprecated alias that points to `reacting-combustion-flow-generic.md`)

Each template is intentionally compact:
- choose a solver-family branch first
- name the minimum critical dictionaries and fields
- flag startup risks early
- give agents a fixed debug order instead of loose tips
