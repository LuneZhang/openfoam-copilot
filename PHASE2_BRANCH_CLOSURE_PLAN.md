# Phase 2 Branch Closure Plan

Date: 2026-03-16
Status: active

## Goal

Turn the current troubleshooting layer from a useful first-pass knowledge base into a **branch-closed routing system** for high-frequency OpenFOAM failures.

The immediate target is not broad topic accumulation. The target is to make an agent reliably answer:
- what failure family is this?
- what should be checked first, second, third?
- when should the diagnosis branch into BC, mesh, parallel, pressure-convention, or numerics paths?
- which steps are backed by official guidance vs bounded community heuristics?

## Current coverage snapshot

### Stronger areas already present
- startup / divergence symptom buckets
- continuity / pressure-anchor triage
- boundary patch typing / `empty` misuse structural failures
- parallel-only failures tied to coupled-patch / cyclicAMI decomposition fragility
- scenario -> playbook -> node routing skeleton

### Why Phase 2 still needs closure work
Current nodes are already useful, but several of them are still **symptom buckets**. They point an agent in the right direction, but do not yet always narrow the problem into the most likely branch-specific subcase.

That means the repository can already reduce random guesswork, but it still needs more branch-specific nodes to reduce search breadth and improve ordered diagnosis.

## Branch-closure principle

For each high-frequency failure family, add enough evidence and routing detail that an agent can move through this chain:

1. classify scenario
2. classify symptom
3. choose playbook
4. land on a small top-ranked node set
5. branch into a narrower node if the first checks confirm a sub-pattern
6. give a prioritized recovery order with source-backed confidence labels

## Priority branch set

### A. Boundary-condition structural closure

#### Why this branch matters
A large share of bad runs are not caused by numerics first. They are caused by structurally wrong BC roles, pressure conventions, missing companion turbulence fields, or field/patch mismatches.

#### Already covered
- `patch-name-boundary-mismatch`
- `illegal-empty-2d-boundary-usage`
- `p-vs-p_rgh-confusion`
- `unremovable-continuity-error-bc-balance`
- `turbulence-field-startup-mismatch`

#### Remaining high-value gaps
1. inlet/outlet role confusion and unsupported backflow behavior
2. turbulence field pair inconsistency beyond generic startup mismatch
3. pressure-anchor placement mistakes split by solver family / buoyancy branch
4. field-to-patch semantic mismatch where dictionary syntax is valid but physics role is wrong

#### Planned outputs
- 2-4 new community source records
- 2-3 narrower troubleshooting nodes
- citation-map expansion for BC-driven failure routing
- possible distilled rule for "structurally valid but physically wrong BC role assignment"

## B. Mesh-quality branch closure

### Why this branch matters
Current mesh handling is still broad. Many real cases fail not because the mesh is globally bad, but because a local region, layer collapse, interface distortion, or decomposition-sensitive defect creates a narrow instability hotspot.

### Already covered
- `mesh-quality-driven-instability`
- `localized-divergence-hotspot-triage`
- playbook support through `mesh-quality-repair-v1`

### Remaining high-value gaps
1. local bad-cell hotspot despite acceptable global `checkMesh`
2. non-orthogonality / skewness causing pressure-correction instability rather than immediate crash
3. boundary-layer / near-wall mesh degeneration interacting with turbulence startup
4. mesh quality problems that only become visible after decomposition or interface partitioning

### Planned outputs
- 2-4 new source records focused on mesh-induced failure signatures
- 2-3 narrower nodes branching out of `mesh-quality-driven-instability`
- one distilled rule for local-hotspot-first diagnosis instead of global numerics thrash

## C. Parallel / decomposition closure

### Why this branch matters
This is one of the highest-value differentiators for an agent-oriented knowledge base. Serial-clean / parallel-bad cases are expensive, confusing, and poorly served by generic official reading alone.

### Already covered
- `parallel-only-failure`
- `parallel-sensitive-interface-decomposition-rule`
- `ami-single-sided-processor-coverage-rule`
- source evidence for coupled patches and cyclicAMI asymmetry

### Remaining high-value gaps
1. decomposition crossing fragile interfaces or thin coupled regions
2. processor-boundary field inconsistency after decomposition
3. branch-specific guidance for "serial OK, low core count OK, larger core count bad"
4. separation of mesh partition defects vs BC/interface semantic defects in parallel-only failures

### Planned outputs
- 2-3 new source records
- 2 narrower nodes under the `parallel-only-failure` branch
- tighter routing language for scale-sensitive failures
- stronger citation-map coverage for parallel branch escalation

## Recommended execution order

### Batch 1 — BC structural closure
Reason:
- highest frequency in setup-class failures
- strongly improves pre-run case review quality
- best complement to the current scenario templates and setup playbooks

### Batch 2 — Parallel closure
Reason:
- highest marginal value over plain official docs + example cases
- strong differentiator for real troubleshooting usefulness
- current evidence base is present but not yet branch-complete

### Batch 3 — Mesh branch closure
Reason:
- benefits from the divergence-localization rule already in place
- easier to add once BC and parallel routing semantics are better separated

## Acceptance standard for each batch

A batch counts as done only if it includes all of the following:
1. new source records
2. new or refined troubleshooting nodes
3. source-index / citation-map updates
4. routing relevance from scenario and/or playbook layer
5. an observable improvement in how an agent orders first checks

## What not to do
- do not bulk-collect loosely related community posts without routing value
- do not create many shallow symptom buckets without narrower branch escalation
- do not let playbooks encode domain claims that are not traceable to source-backed nodes
- do not over-polish official notes while branch-specific troubleshooting remains underpowered

## Short conclusion
The next best move is **not** more generic documentation accumulation.
The next best move is to make the troubleshooting graph more branch-specific, especially for:
- BC structural failures
- parallel-only failures
- mesh-localized instability

That is the fastest path from "knowledge base" to "agent-usable debugging system".
