# Solver Family Map v1

## Purpose
Provide a first-pass mapping from problem traits to OpenFOAM solver families.
This map is intentionally coarse and should be used before detailed dictionary work.

## Decision axes
1. incompressible vs compressible
2. steady vs transient
3. single-phase vs multiphase
4. is heat transfer / buoyancy present?
5. is combustion / species transport present?

## Coarse mapping

### Incompressible, single-phase
Use when:
- density variation is negligible
- baseline internal/external flow is the target
- the main questions are velocity-pressure behavior and turbulence choice

Watch for:
- `U` / `p` field consistency
- SIMPLE vs PISO/PIMPLE workflow mismatch
- turbulence field requirements when RANS/LES is enabled

### Compressible / thermo-coupled
Use when:
- density changes matter
- thermal coupling matters strongly
- energy equation is central to the case

Watch for:
- thermo package consistency
- extra property dictionaries
- pressure variable conventions and energy setup

### Buoyant family
Use when:
- gravity-driven or thermo-buoyant behavior matters
- natural convection or mixed buoyancy is central

Watch for:
- gravity setup
- `p_rgh`-style conventions where applicable
- temperature and buoyancy-related boundary consistency

### Multiphase family
Use when:
- multiple phases or interfaces are essential
- free-surface or dispersed-phase behavior is central

Watch for:
- additional phase fields
- interface-specific numerics sensitivity
- tighter stability demands

### Reacting / combustion / species family
Use when:
- chemistry, species transport, or heat release is central

Watch for:
- thermo/chemistry coupling consistency
- additional fields and source terms
- strong stability sensitivity during initialization

## Default solver-selection workflow
1. write the physics statement in one sentence
2. classify it by the five decision axes above
3. identify the closest official tutorial family
4. adopt that family’s structural pattern before tuning numerics
5. only then refine solver choice and model details

## Common misclassification patterns
- choosing incompressible because the geometry is familiar, even when thermal density effects matter
- choosing a steady workflow when the physically relevant behavior is transient
- reusing a single-phase template for a multiphase problem
- treating solver choice as secondary to turbulence-model choice

## Usage rule
This file is a routing tool, not a final authority. Use it to choose the right branch of knowledge first; then move to official solver notes and case-setup playbooks.
