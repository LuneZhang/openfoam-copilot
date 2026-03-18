# Parallel Triage Decision Tree

## Purpose

Provide a compact, agent-usable decision path for OpenFOAM cases that are stable or partly stable in serial, but become suspicious only after decomposition and parallel launch.

This file is not a replacement for the detailed troubleshooting nodes.
Its job is to decide **which parallel branch to enter first**.

## When to use this tree

Use this tree when any of the following is true:
- serial is clean or cleaner than parallel
- only parallel runs diverge or crash
- higher processor counts make the case worse
- processor-local logs show more useful clues than reconstructed fields
- failure localizes near AMI / cyclic / coupled / interface / outlet / hotspot regions after decomposition

Do **not** start here if the serial case is already clearly broken for structural reasons.
In that case, fix the serial branch first.

---

## Step 0 — Is serial actually clean?

### If **no**
Do not treat this as a parallel-rooted case yet.
Route back to the structural branch first:
- BC structure
- mesh hotspot
- solver/model mismatch
- pressure convention / anchoring
- turbulence-field consistency

### If **yes**
Continue.
This means decomposition may be creating a new failure surface rather than simply speeding up an old one.

Primary parent node:
- `parallel-only-failure`

---

## Step 1 — Does the failure appear only beyond a processor-count threshold?

Examples:
- serial OK
- 2 ranks OK
- 4 ranks marginal
- 8+ ranks fail

### If **yes**
Prefer this branch first:
- `processor-count-sensitive-parallel-failure`

What the agent should check first:
1. compare low-rank and failing-rank decomposition layouts
2. ask whether sensitive interfaces or hotspots are being split more aggressively at higher rank counts
3. inspect processor-local logs at the failing rank count
4. avoid assuming that “more ranks = same case, only faster”

Most likely interpretation:
- decomposition geometry changed enough to create a new failure class

### If **no**
Continue.
This suggests the case is generically parallel-bad, not only scale-sensitive.

---

## Step 2 — Is processor-local evidence stronger than reconstructed global evidence?

Clues:
- one processor reports the first useful patch / topology / AMI / coupled mismatch
- reconstructed fields only show global damage after the fact
- processor-local boundary files reveal asymmetry or mismatch not obvious in the reconstructed case

### If **yes**
Prefer this branch first:
- `processor-boundary-field-inconsistency`

What the agent should check first:
1. read processor-local logs before trusting reconstructed fields
2. inspect processor-local boundary ownership and local patch representation
3. use reconstruction later for confirmation, not as the first truth source

Most likely interpretation:
- the first useful clue exists on processor boundaries or rank-local field behavior

### If **no**
Continue.
This means the failure is not primarily being diagnosed from processor-local mismatch clues.

---

## Step 3 — Did parallelization fragment a fragile hotspot, or merely expose a structural interface defect sooner?

This is the main discriminator when failure stays near an interface/opening/hotspot region.

### Branch A — decomposition fragmented a hotspot
Favor this interpretation when:
- changing decomposition layout moves or reshapes the failing region
- the same physical area was already weak in serial / low-rank runs
- the suspect region also overlaps with local mesh weakness, sharp gradients, plume/wake recirculation, or small geometric features
- the interface looks suspicious mainly because that is where the fragmented hotspot first shows up

Route toward:
- `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- often then down to `critical-region-local-mesh-hotspot`

Likely fix direction:
- protect the region better in decomposition
- improve local mesh / local startup strategy
- reduce fragmentation of the sensitive zone

### Branch B — interface / boundary semantics were already wrong
Favor this interpretation when:
- the problem stays tied to the same physical patch/interface regardless of decomposition layout
- serial already showed weak symptoms at the same location, even if it did not fully fail
- reverse flow, pressure pairing, AMI/coupled assumptions, or companion fields are structurally suspicious
- parallel execution only made the semantic defect fail earlier or more clearly

Route toward:
- `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- then into the narrower structural node:
  - `outlet-backflow-role-confusion`
  - `buoyant-pressure-anchor-reference-mismatch`
  - `turbulence-field-family-patch-role-mismatch`
  - or another BC/interface semantic node

Likely fix direction:
- repair interface / BC semantics first
- do not spend all effort on decomposition before the structural defect is removed

---

## Fast routing summary

### Parallel problem, first pass
1. serial clean?  
   - no → leave parallel tree, fix structural branch first
   - yes → `parallel-only-failure`

2. only fails after higher rank count?  
   - yes → `processor-count-sensitive-parallel-failure`
   - no → continue

3. processor-local clues stronger than reconstructed global clues?  
   - yes → `processor-boundary-field-inconsistency`
   - no → continue

4. interface/hotspot ambiguity remains?  
   - yes → `decomposition-fragmented-hotspot-vs-interface-semantic-defect`

---

## Anti-patterns

Do not let the agent do these too early:
- immediately retune numerics before comparing serial vs parallel behavior
- trust reconstructed global fields more than processor-local first-failure evidence
- assume all interface-local parallel failures are decomposition bugs
- assume all parallel-only failures are mesh problems
- keep increasing processor count without checking whether the decomposition layout itself changed the failure mode

---

## Recommended companion files

For parallel troubleshooting, read alongside this file:
- `ontology/troubleshooting-graph/nodes/parallel-only-failure.md`
- `ontology/troubleshooting-graph/nodes/processor-count-sensitive-parallel-failure.md`
- `ontology/troubleshooting-graph/nodes/processor-boundary-field-inconsistency.md`
- `ontology/troubleshooting-graph/nodes/decomposition-fragmented-hotspot-vs-interface-semantic-defect.md`
- `knowledge/distilled/parallel-sensitive-interface-decomposition-rule.md`
- `knowledge/distilled/ami-single-sided-processor-coverage-rule.md`

## Source references

- `official-openfoam-user-guide-parallel`
- `official-openfoam-decomposePar-guide`
- `official-openfoam-user-guide-boundary-conditions`
- `official-openfoam-user-guide-checkMesh`
- `community-openfoam-bugtracker-coupled-patch-parallel-crash`
- `community-openfoam-bugtracker-cyclicami-single-sided-parallel-crash`
- `community-simscale-kb-divergence-localization`
