# Phase 1 Progress

Date: 2026-03-16
Status: current troubleshooting-foundation pass closed; ready to transition

## Completed in this pass

### Official backbone
- `knowledge/official/transport/transportProperties-basics.md`
- `knowledge/official/turbulence/turbulenceProperties-activation-basics.md`

### Tutorial pattern extraction seeds
- `knowledge/tutorials/tutorial-pattern-extraction-seeds.md`

### Source-triage prompt and community framework
- `prompts/source-triage-assistant.md`
- `knowledge/community/source-triage-framework.md`
- `knowledge/community/troubleshooting-source-buckets-v1.md`

### Scenario-template batch 1
- `scenario_templates/README.md`
- `scenario_templates/incompressible-laminar-internal-flow.md`
- `scenario_templates/incompressible-rans-external-aerodynamics.md`
- `scenario_templates/buoyant-natural-convection-room-scale.md`

### Community-source records batch 1
- `knowledge/community/source-records/simscale-floating-point-exception-kb.md`
- `knowledge/community/source-records/simscale-relaxation-factors-doc.md`
- `knowledge/community/source-records/simscale-forum-floating-point-thread.md`

### Troubleshooting nodes batch 1
- `ontology/troubleshooting-graph/nodes/floating-point-exception-startup.md`
- `ontology/troubleshooting-graph/nodes/steady-state-divergence-overaggressive-numerics.md`

### Project bookkeeping updates
- updated `PHASE1_BACKLOG.md`
- updated `knowledge/community/README.md`
- updated `ontology/troubleshooting-graph/README.md`
- updated `references/source-index.yaml`
- updated `references/citation-map.yaml`

## Phase estimate

Approximate Phase 1 completion: **100% for the current troubleshooting-foundation pass**

Reasoning:
- official backbone priority set is usable at baseline-note level for the current routing workflow
- scenario -> playbook -> node routing is now in place and reflected in entry docs and prompt layer
- troubleshooting graph now contains meaningful branch-specific BC / mesh / parallel nodes instead of only generic symptom buckets
- top-level troubleshooting entry and parallel triage decision paths now exist, so the current troubleshooting-foundation pass is complete

## Next-stage priorities
1. add / refine scenario templates for compressible, multiphase, and reacting branches
2. official backbone polish for pressure-variable conventions, runtime observability, and solver-family-to-template mapping
3. validate that the current routing workflow generalizes cleanly into the new scenario families
4. patch only the routing gaps that block scenario expansion, rather than reopening broad troubleshooting sprawl

## Notes
- The current troubleshooting-foundation pass is closed.
- This file now functions as a closeout summary for the current pass and a handoff into the next-stage scenario expansion work.
- This progress file is also used as the current task-guard done marker.

## Additional progress in later passes
- added second batch of troubleshooting nodes
- connected scenario templates to playbooks and troubleshooting nodes
- strengthened prompt layer and agent entry workflow
- cleaned source index and added retrieval / traceability rules
- expanded Phase 2 community troubleshooting evidence for boundary-condition structural failures with two new community source records (`community-simscale-kb-inconsistent-patch-patchfield`, `community-simscale-kb-empty-2d-boundary`)
- added distilled troubleshooting node `ontology/troubleshooting-graph/nodes/illegal-empty-2d-boundary-usage.md`
- strengthened citation traceability for boundary-condition mismatch routing in `references/citation-map.yaml`
- expanded Phase 2 community troubleshooting evidence for divergence-localization workflow with new source record `community-simscale-kb-divergence-localization`
- added troubleshooting node `ontology/troubleshooting-graph/nodes/localized-divergence-hotspot-triage.md`
- added first distilled troubleshooting rule `knowledge/distilled/divergence-hotspot-localization-rule.md`
- extended source/citation traceability for the new divergence-localization evidence cluster
- expanded Phase 2 community troubleshooting evidence for parallel-only failures with source record `community-openfoam-bugtracker-coupled-patch-parallel-crash`
- added distilled rule `knowledge/distilled/parallel-sensitive-interface-decomposition-rule.md` to route serial-clean/parallel-bad cases through decomposition-sensitive interface checks
- strengthened citation traceability for `parallel-only-failure` via `references/citation-map.yaml`
- expanded Phase 2 community troubleshooting evidence for cyclicAMI/AMI parallel asymmetry with new source record `community-openfoam-bugtracker-cyclicami-single-sided-parallel-crash`
- added distilled rule `knowledge/distilled/ami-single-sided-processor-coverage-rule.md` to route serial-clean / scale-sensitive AMI failures through processor-local interface coverage checks
- strengthened citation traceability for parallel interface fragility by wiring the new AMI evidence into `parallel-only-failure` and the parallel distilled rules
- expanded Phase 2 community troubleshooting evidence for continuity / pressure-anchoring failures with new source record `community-simscale-kb-continuity-error`
- added troubleshooting node `ontology/troubleshooting-graph/nodes/unremovable-continuity-error-bc-balance.md`
- extended source/citation traceability so continuity-error routing now distinguishes BC-balance / fixed-pressure-anchor mistakes from later-stage generic continuity growth
- expanded Phase 2 BC structural evidence for outlet backflow / inlet-outlet role confusion with new source record `community-simscale-docs-pressure-outlet-backflow`
- added troubleshooting node `ontology/troubleshooting-graph/nodes/outlet-backflow-role-confusion.md`
- updated playbook routing so divergence recovery and BC design can branch into reverse-flow-at-outlet diagnosis earlier
- expanded Phase 2 BC structural evidence for buoyant pressure-anchor / reference-height mistakes with new source record `community-simscale-docs-modified-pressure-reference`
- added troubleshooting node `ontology/troubleshooting-graph/nodes/buoyant-pressure-anchor-reference-mismatch.md`
- updated buoyant scenario and BC-design routing so agent paths now distinguish wrong pressure variable from wrong modified-pressure anchoring
- expanded Phase 2 BC/turbulence-structure evidence for RANS turbulence-field family / patch-role mistakes with new source records `community-simscale-docs-k-epsilon-guidance` and `community-simscale-docs-k-omega-sst-guidance`
- added troubleshooting node `ontology/troubleshooting-graph/nodes/turbulence-field-family-patch-role-mismatch.md`
- updated RANS scenario and BC-design routing so agent paths now distinguish missing turbulence fields from wrong turbulence-family semantics on walls and openings
- expanded Phase 2 mesh evidence for critical-region local mesh hotspots with new source records `community-simscale-docs-mesh-quality-visualization` and `community-simscale-docs-non-orthogonal-correctors`
- added troubleshooting node `ontology/troubleshooting-graph/nodes/critical-region-local-mesh-hotspot.md`
- updated mesh-repair and scenario routing so agent paths now distinguish globally passable meshes from locally poisonous bad-cell pockets
- expanded Phase 2 parallel evidence for processor-count-sensitive failures by splitting rank-threshold behavior out from generic `parallel-only-failure`
- added troubleshooting node `ontology/troubleshooting-graph/nodes/processor-count-sensitive-parallel-failure.md`
- updated divergence and scenario routing so agent paths now distinguish generic parallel-only failure from decomposition layouts that become pathological only after scaling rank count
- expanded Phase 2 parallel evidence for processor-boundary inconsistency / reconstruction masking using existing coupled-patch and cyclicAMI source records
- added troubleshooting node `ontology/troubleshooting-graph/nodes/processor-boundary-field-inconsistency.md`
- updated parallel routing so agent paths now prioritize processor-local evidence when reconstructed global output hides the first useful clue
- expanded Phase 2 parallel discrimination for decomposition-fragmented hotspots vs pre-existing interface semantic defects
- added troubleshooting node `ontology/troubleshooting-graph/nodes/decomposition-fragmented-hotspot-vs-interface-semantic-defect.md`
- updated parallel escalation paths so agent routes can now separate decomposition-created failure classes from structural interface defects merely exposed sooner in parallel
- added `PARALLEL_TRIAGE_DECISION_TREE.md` to compress the new parallel branches into a direct agent decision path
- added `TROUBLESHOOTING_ENTRY.md` as the top-level troubleshooting entry before scenario/playbook/node routing
- updated `prompts/troubleshooting-assistant.md` so the prompt layer now reflects the newer BC / mesh / parallel routing behavior instead of the older flatter workflow
- added `PHASE1_STAGE_GATE.md` and `NEXT_STAGE_STARTUP_CHECKLIST.md` so the repository now has explicit close-current-pass and start-next-stage criteria
- updated `README.md` and `AGENT_ENTRY.md` so agents can enter the troubleshooting tree without scanning every node first

