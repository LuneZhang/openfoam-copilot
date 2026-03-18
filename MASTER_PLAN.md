# OpenFOAM Tutorial for Agent — Master Plan

## Project Goal
Build a high-quality, agent-oriented OpenFOAM knowledge engineering project that lets an agent:
- choose suitable solvers and case structures
- set up reasonable cases and key dictionaries
- diagnose and fix common divergence / crash / nonphysical-result problems
- use official documentation as the primary source of truth
- use high-value community troubleshooting knowledge as secondary support

This project is **not** trying to scrape “everything on the internet”. It is designed to create a **high-value, structured, reusable OpenFOAM knowledge base** for agents.

## Scope
### Include
- OpenFOAM official documentation and guides
- official tutorials and solver documentation
- high-value community troubleshooting discussions
- reusable case-setup and debugging workflows
- structured error taxonomy and troubleshooting graph

### Exclude
- low-quality duplicate blogspam
- unverifiable folklore
- irrelevant source-code internals with no case-setup/debug value
- blind bulk scraping without curation

## Delivery Strategy
Deliver in phases so quality can be reviewed and corrected early.

### Phase 0 — Project scaffold + schemas
Outputs:
- project directory structure
- source registry schema
- knowledge note schema
- troubleshooting node schema
- agent entry document

### Phase 1 — Official backbone
Priority topics:
- case directory anatomy
- solver families and applicability
- controlDict / fvSchemes / fvSolution
- turbulence, thermo, transport properties
- boundary conditions
- mesh quality
- official tutorial patterns

Outputs:
- knowledge/official/
- ontology/concepts/
- ontology/solver-maps/
- playbooks/case-setup/

### Phase 2 — Community troubleshooting layer
Priority problem families:
- floating point exception
- continuity error too large
- residual blow-up / no convergence
- bad mesh / non-orthogonality / skewness
- bad BC / bad initialization
- timestep / Courant problems
- turbulence-model instability
- parallel / decomposition issues

Outputs:
- knowledge/community/
- ontology/error-taxonomy/
- ontology/troubleshooting-graph/
- playbooks/divergence-recovery/
- playbooks/debug-workflows/

### Phase 3 — Typical engineering scenario templates
Priority scenario families:
- incompressible internal flow
- external aerodynamics
- heat transfer
- multiphase
- reacting / combustion
- steady vs transient
- laminar vs RANS

Outputs:
- examples/
- playbooks/turbulence-model-selection/
- playbooks/boundary-condition-design/
- playbooks/mesh-quality-repair/

### Phase 4 — Agent interface layer
Outputs:
- AGENT_ENTRY.md
- prompts/setup-assistant.md
- prompts/troubleshooting-assistant.md
- prompts/case-review.md
- reusable decision workflows

## Quality Rules
1. Every important conclusion must be traceable to a source.
2. Official guidance and community heuristics must be clearly separated.
3. Every troubleshooting recipe must be actionable, not vague.
4. Knowledge must be optimized for agent reuse, not human essay reading.
5. High-risk recommendations must include applicability limits.

## Core Design Principle
Three layers:
1. Raw curated source layer
2. Distilled reusable knowledge layer
3. Operational playbook / troubleshooting workflow layer

## Recommended Build Order
1. Create schemas and project skeleton
2. Build official backbone first
3. Add community troubleshooting second
4. Add scenario templates third
5. Add agent-facing prompts and routing last

## Success Standard
An agent using this project should be able to:
- explain why a solver or model is chosen
- propose a reasonable first-pass case setup
- inspect dictionaries and spot likely configuration mistakes
- respond to common OpenFOAM errors with a prioritized debugging path
- distinguish high-confidence official rules from lower-confidence community heuristics
