# OpenFOAM Tutorial for Agent — Detailed Design v2

## 1. Project Directory Layout

```text
openfoam-tutorial-for-agent/
├── MASTER_PLAN.md
├── README.md
├── AGENT_ENTRY.md
├── schemas/
│   ├── source-record.schema.yaml
│   ├── knowledge-note.schema.yaml
│   ├── troubleshooting-node.schema.yaml
│   ├── solver-profile.schema.yaml
│   └── scenario-template.schema.yaml
├── references/
│   ├── source-index.yaml
│   ├── citation-map.yaml
│   ├── trust-ranking.md
│   └── collection-policy.md
├── knowledge/
│   ├── official/
│   │   ├── case-structure/
│   │   ├── solvers/
│   │   ├── numerics/
│   │   ├── turbulence/
│   │   ├── thermo/
│   │   ├── boundary-conditions/
│   │   ├── mesh/
│   │   └── parallel/
│   ├── tutorials/
│   │   ├── incompressible/
│   │   ├── compressible/
│   │   ├── multiphase/
│   │   ├── heat-transfer/
│   │   └── combustion/
│   ├── community/
│   │   ├── divergence/
│   │   ├── mesh-errors/
│   │   ├── bc-errors/
│   │   ├── solver-selection/
│   │   ├── parallel/
│   │   └── performance/
│   └── distilled/
│       ├── design-rules/
│       ├── failure-patterns/
│       ├── solver-choice/
│       └── parameter-effects/
├── ontology/
│   ├── concepts/
│   ├── solver-maps/
│   ├── error-taxonomy/
│   ├── troubleshooting-graph/
│   └── scenario-graphs/
├── playbooks/
│   ├── case-setup/
│   ├── solver-selection/
│   ├── turbulence-model-selection/
│   ├── boundary-condition-design/
│   ├── initialization/
│   ├── mesh-quality-repair/
│   ├── divergence-recovery/
│   ├── residual-diagnosis/
│   ├── parallel-debug/
│   └── postprocessing-diagnosis/
├── examples/
│   ├── incompressible/
│   ├── compressible/
│   ├── multiphase/
│   ├── heat-transfer/
│   └── combustion/
├── prompts/
│   ├── setup-assistant.md
│   ├── troubleshooting-assistant.md
│   ├── case-review.md
│   └── source-triage.md
└── tools/
    ├── collectors/
    ├── normalizers/
    ├── checkers/
    └── builders/
```

## 2. Meaning of Each Top-Level Area

### `schemas/`
Store strict templates so new knowledge is added consistently.

### `references/`
Store source registry, trust rules, citation mapping, and collection policy.

### `knowledge/official/`
Store curated official knowledge summaries by topic.

### `knowledge/tutorials/`
Store distilled patterns from official tutorials, organized by physics/problem class.

### `knowledge/community/`
Store curated, source-linked troubleshooting notes from community posts.

### `knowledge/distilled/`
Store reusable conclusions that cut across many sources.

### `ontology/`
Store compact knowledge maps that agents can traverse:
- solver -> suitable physics
- symptom -> likely causes
- error -> first checks
- scenario -> recommended workflow

### `playbooks/`
Store operational procedures for setup and debugging.

### `examples/`
Store scenario-specific templates and high-level patterns, not raw copied tutorials.

### `prompts/`
Store agent-facing task prompts so another agent can use the knowledge base correctly.

### `tools/`
Store collection / normalization / validation helpers for maintaining the knowledge base.

## 3. Required Schema Types

### 3.1 Source Record
Used for every official page, tutorial page, or community post.

Fields:
- id
- title
- source_type
- source_name
- url
- date
- trust_level
- tags
- solver_scope
- physics_scope
- summary
- key_points
- applicability
- caveats

### 3.2 Knowledge Note
Used for distilled reusable knowledge.

Fields:
- id
- title
- problem_class
- prerequisites
- recommendation
- rationale
- source_refs
- confidence
- failure_modes
- anti_patterns

### 3.3 Troubleshooting Node
Used for symptoms/errors and debugging flow.

Fields:
- id
- symptom
- probable_causes
- first_checks
- deeper_checks
- likely_fixes
- escalation_path
- source_refs
- confidence

### 3.4 Solver Profile
Used to map solver families to problem classes.

Fields:
- solver_name
- physics_type
- steady_or_transient
- compressibility
- turbulence_support
- common_use_cases
- common_failure_modes
- setup_watchpoints

### 3.5 Scenario Template
Used for typical application classes.

Fields:
- scenario_name
- typical_solver_choices
- key_dictionaries
- initialization_guidance
- turbulence_guidance
- mesh_guidance
- stability_risks
- debug_priority_order

## 4. Phase 1 Collection Priorities

### Priority Group A — Official fundamentals
1. Case directory structure
2. controlDict
3. fvSchemes
4. fvSolution
5. transportProperties
6. turbulenceProperties
7. thermophysicalProperties
8. boundary conditions basics
9. checkMesh and mesh quality guidance
10. solver overview pages

### Priority Group B — Official tutorial patterns
Extract reusable patterns from representative tutorials for:
- incompressible laminar
- incompressible turbulent
- compressible flow
- conjugate heat transfer
- multiphase
- reacting flow

### Priority Group C — High-frequency troubleshooting topics
1. floating point exception
2. non-convergence / exploding residuals
3. continuity error growth
4. Courant number too high
5. bad mesh warnings
6. wrong/missing boundary conditions
7. parallel decomposition issues
8. nonphysical values (negative temperature/density/etc.)

## 5. Trust Policy

### High trust
- official OpenFOAM docs
- official tutorials
- official repository documentation

### Medium trust
- expert community discussions with reproducible reasoning
- widely repeated and source-supported troubleshooting posts

### Low trust
- anecdotal tips without validation
- isolated blog advice with no source chain

Rule: low-trust items may be stored, but must be marked clearly and never presented as canonical rules.

## 6. Agent Routing Policy

### Use official knowledge first when:
- selecting solver families
- interpreting dictionary semantics
- checking syntax / file structure
- identifying documented limits and assumptions

### Use community troubleshooting when:
- official docs are too abstract for debugging
- diagnosing divergence patterns
- interpreting symptom clusters from real cases
- prioritizing practical recovery steps

### Use playbooks when:
- the task is setup or debugging, not passive explanation

## 7. Phase 1 Deliverables

At the end of Phase 1, the project should already contain:
- project skeleton
- schemas
- source registry
- official backbone topic notes
- first solver map
- first case-setup playbook
- first troubleshooting taxonomy draft
- agent entry instructions

## 8. What Makes This Useful to Agents

This project is only successful if another agent can quickly answer:
- what solver should I use?
- what dictionaries matter most?
- what boundary conditions are likely wrong?
- why is the case diverging?
- what should I check first, second, third?

So every document must optimize for:
- retrieval
- prioritization
- applicability boundaries
- debugging order
