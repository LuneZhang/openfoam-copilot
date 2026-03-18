# Validation Workflow

Date: 2026-03-16
Status: active; first manual audit batch underway

## Purpose

Define how to validate the current routing system after the first-pass scenario expansion.

The goal is not to prove perfect correctness.
The goal is to verify that agents now choose better first branches, better first checks, and better escalation order than before.

## Validation order

### Step 1 — pick a representative case class
Start from `VALIDATION_CASE_MATRIX.md`.
Choose one case class at a time.

### Step 2 — present the case as an agent task
Use the repository normally:
1. identify the scenario family
2. load the scenario-to-node routing
3. load the relevant playbook
4. load the top 1–3 nodes
5. inspect the produced diagnosis order

### Step 3 — compare against expected routing
Check:
- did the scenario family match expectation?
- did the agent choose the expected first branch class?
- did it avoid obvious anti-patterns?
- did it escalate coherently if the first branch failed?

### Step 4 — classify the result
Use one of these labels:
- pass
- weak-pass
- misrouted
- incomplete

### Step 5 — patch only the failing layer
If validation fails, patch the shallowest layer that explains the miss:
1. scenario template
2. scenario-to-node routing
3. playbook-to-node routing
4. prompt-layer wording
5. only then add a new node or new source evidence

## Anti-patterns

Do not validate by:
- adding new nodes before understanding the routing miss
- patching three layers at once when only one failed
- treating every failure as a source-coverage problem
- letting one scenario family monopolize the whole validation cycle

## Success criteria for this validation path

The validation path is successful if:
1. the three scenario families consistently route into sensible first branches
2. setup-class failures are identified before generic numerics tuning
3. local hotspot cases are not flattened into global-average reasoning
4. parallel-sensitive cases still route through the dedicated parallel tree
5. validation findings lead to narrow, justified fixes rather than fresh sprawl

## Recommended cadence

1. validate one compressible case class
2. validate one multiphase case class
3. validate one reacting case class
4. compare where the routing still feels asymmetric
5. only then decide whether to deepen one scenario family or keep validating
