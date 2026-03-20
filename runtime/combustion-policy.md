# Combustion Family Policy

This policy defines the combustion expansion wave that sits on top of the existing runtime spine.

## Family Priority Order

Exactly five narrow combustion families are active in this wave, in this priority order:

1. `premixed-combustion-baseline`
2. `nonpremixed-diffusion-flame`
3. `buoyant-fire-compartment`
4. `partially-premixed-recirculating-combustor`
5. `spray-combustion`

Do not add a sixth family in this pass.
Do not add engine-combustion taxonomy in this pass.

## Parent Template Rule

`reacting-combustion-flow-generic` remains active.
Use it as the parent and fallback template when the case is clearly reacting but the evidence does not yet support one narrow family.

Use a narrow family only when the case statement, solver lineage, and first-check order are all clearly narrower than the generic reacting branch.

## Primary solver and tutorial anchors

- `premixed-combustion-baseline` -> `XiFoam`
- `nonpremixed-diffusion-flame` -> `reactingFoam`
- `buoyant-fire-compartment` -> `fireFoam`
- `partially-premixed-recirculating-combustor` -> `XiFoam` as the primary premixed anchor, with explicit recirculation and return-state review
- `spray-combustion` -> `sprayFoam`

## Source and traceability rule

- Official solver and tutorial anchors stay primary.
- Community evidence may narrow troubleshooting order, but it does not replace official setup semantics.
- `fireFoam` and `sprayFoam` must carry explicit distribution and version scope in `runtime/catalog/sources.json`.
- If a future combustion addition cannot name an official anchor, a justified narrow node, and a replay fixture, it does not land.

## Node Justification Checklist

Add a combustion troubleshooting node only when all three conditions hold:

1. it has a distinct first-check order that is not already covered by a generic reacting node
2. it has explicit source backing in `references/source-index.yaml`
3. it has at least one routing replay fixture proving why the branch exists

## Version Sensitivity

- `XiFoam`-anchored premixed and partially premixed families are relatively stable across the currently targeted OpenFOAM distributions, but they still inherit solver-family and tutorial-lineage differences.
- `reactingFoam` remains moderately distribution/version sensitive because thermo and chemistry setup details drift more than pure family naming suggests.
- `fireFoam` must stay explicitly distribution- and version-tagged because buoyant fire, ventilation, and radiation behavior differs materially across OpenFOAM variants.
- `sprayFoam` must stay explicitly distribution- and version-tagged because injection, parcel, and evaporation behavior is more version-sensitive than the simpler reacting families.

## Routing rule

Route by family first, then by playbook, then by node.
Do not bypass the runtime spine with a second combustion routing source.

## Validation rule

Combustion routing is validated through:

- the scenario and node catalogs
- the debug-routing playbooks
- the split combustion fixture files under `runtime/fixtures/routing/`
- the D-block in `VALIDATION_CASE_MATRIX.md`
