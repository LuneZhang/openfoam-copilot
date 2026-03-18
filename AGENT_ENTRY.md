# AGENT_ENTRY.md

This project is an agent-oriented OpenFOAM knowledge base.

## Mission
Use this repository to help an agent:
- choose suitable solver families
- set up OpenFOAM cases correctly
- review dictionaries and case structure
- diagnose divergence, crashes, and nonphysical results
- separate official rules from community heuristics

## Reading order for agents

### For case setup tasks
1. `README.md`
2. `playbooks/case-setup/README.md`
3. `ontology/solver-maps/README.md`
4. Relevant topic under `knowledge/official/`
5. Relevant scenario under `scenario_templates/`

### For troubleshooting tasks
1. if a case path is available, run the first-pass auto-intake workflow from `CASE_AUTO_INTAKE_SPEC.md`
2. read `TROUBLESHOOTING_ENTRY.md`
3. identify the closest file under `scenario_templates/`
4. read `playbooks/debug-routing/scenario-to-node-routing-v1.md`
5. if the symptom is parallel-sensitive, read `PARALLEL_TRIAGE_DECISION_TREE.md`
6. select the best matching playbook
7. read `playbooks/debug-routing/playbook-to-node-routing-v1.md`
8. load the top matching troubleshooting nodes under `ontology/troubleshooting-graph/nodes/`
9. then consult `knowledge/community/` and `knowledge/official/` as evidence layers

### For source collection / maintenance tasks
1. `references/collection-policy.md`
2. `references/trust-ranking.md`
3. `schemas/source-record.schema.yaml`
4. `references/source-index.yaml`

## Hard rules
- Prefer official OpenFOAM documentation over community advice when they conflict.
- Treat community posts as heuristics unless corroborated.
- Always preserve source traceability for important claims.
- Do not present low-confidence community tips as canonical truth.
- When debugging, produce a prioritized check order instead of a flat list.
- When setting up a case, explain solver / model / BC choices with assumptions.

## Repository map
- `knowledge/official/` — curated official knowledge by topic
- `knowledge/tutorials/` — reusable patterns extracted from official tutorials
- `knowledge/community/` — curated troubleshooting notes from high-value community sources
- `knowledge/distilled/` — distilled reusable rules and failure patterns
- `ontology/` — compact maps for solver choice, error classes, and troubleshooting traversal
- `playbooks/` — operational setup and debugging workflows
- `scenario_templates/` — scenario-oriented templates and patterns
- `schemas/` — strict storage formats for knowledge items
- `references/` — registry, trust policy, and citation management

## Current project state
The current troubleshooting-foundation pass is complete. The project already contains official backbone notes, scenario templates, troubleshooting nodes, routing docs, top-level troubleshooting entry points, prompt-layer behavior aligned with the routing workflow, and a first-pass path-driven case auto-intake layer. Agents should use scenario -> playbook -> node routing before broad source search.
