# Community Troubleshooting Source Buckets v1

id: community-troubleshooting-source-buckets-v1
problem_class: convergence
confidence: medium
source_refs:
- community-triage-policy-seed

## Why this note exists

Before collecting individual forum threads or issue discussions, Phase 1 needs a source-bucket map. This prevents random ingestion and keeps collection focused on troubleshooting value classes that are likely to generalize.

## Bucket A — recurring startup and dictionary errors

Target symptoms:
- missing field / missing keyword / wrong patch name
- solver starts with obviously wrong field set
- startup aborts after parsing dictionaries

Likely future schema target:
- `TroubleshootingNode`

Reason to collect:
- these failures are common
- they often reveal structural anti-patterns agents can detect early

## Bucket B — divergence and residual blow-up threads

Target symptoms:
- residual explosion
- floating point exception
- continuity error growth
- unstable pressure-velocity coupling

Likely future schema target:
- `TroubleshootingNode` plus playbook reinforcement

Reason to collect:
- strong community value if the thread clearly distinguishes mesh, BC, numerics, and timestep causes

## Bucket C — turbulence and wall-treatment mismatch

Target symptoms:
- bad near-wall behavior
- turbulence fields missing or inconsistent
- wall-function misuse
- model choice causing unstable startup

Likely future schema target:
- `KnowledgeNote`

Reason to collect:
- official docs explain models, but community sources often reveal common misconfiguration patterns

## Bucket D — thermo / buoyancy / `p_rgh` confusion

Target symptoms:
- thermal cases using incompressible assumptions incorrectly
- gravity enabled but pressure treatment inconsistent
- temperature BCs fighting flow setup

Likely future schema target:
- `TroubleshootingNode`

Reason to collect:
- this is a common branch where users copy incompressible intuition into buoyant cases

## Bucket E — mesh-quality-to-instability correlations

Target symptoms:
- `checkMesh` warnings dismissed too early
- instability linked to skewness/non-orthogonality/local bad cells
- fixes involving mesh cleanup vs numerics damping

Likely future schema target:
- `KnowledgeNote`

Reason to collect:
- community posts often contain practical interpretation heuristics absent from terse official references

## Bucket F — parallel-only failure reports

Target symptoms:
- case sane in serial, broken in parallel
- bad decomposition strategy
- reconstruction mismatch or processor-local instability

Likely future schema target:
- `TroubleshootingNode`

Reason to collect:
- useful for keeping parallel debugging separate from base-case instability

## Bucket G — case-specific anecdotes to avoid overfitting

Target symptoms:
- custom solver quirks
- code patching advice
- hardware/compiler specific failures
- highly specialized chemistry or industrial workflows

Likely target:
- references only until a reusable pattern emerges

Reason to collect:
- still useful as evidence inventory, but too risky for immediate distillation

## Recommendation

Start community triage with Buckets A, B, D, and E. They have the best ratio of reuse value to folklore risk.

## Rationale

- Phase 1 needs a collection frame before collection volume grows.
- Buckets align with the existing error-taxonomy and playbook structure.
- This will make later batch ingestion easier to parallelize and audit.

## Applicability limits

- Some source threads span multiple buckets.
- Bucket assignment is a triage aid, not a substitute for source-level judgment.
