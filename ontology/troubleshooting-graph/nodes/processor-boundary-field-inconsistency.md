# Troubleshooting Node — Processor-Boundary Field Inconsistency / Reconstruction Masking

id: processor-boundary-field-inconsistency
symptom: A parallel run shows strange field behavior, patch-area mismatch hints, rank-local anomalies, or inconsistent processor-level diagnostics, but the reconstructed global case hides or smooths over where the inconsistency first appeared.

probable_causes:
- field or patch behavior becomes inconsistent across processor boundaries after decomposition, especially near coupled, cyclic, AMI, or custom interfaces
- the first useful failure evidence exists in processor-local logs or processor-local boundary files rather than in reconstructed fields
- reconstruction or aggregate output makes the case look more uniformly bad than it actually was, masking the first failing processor-local region
- decomposition changed boundary ownership enough that one processor sees a pathological local pairing not obvious in the global view
- users inspect only reconstructed results and miss processor-local mismatch clues that would identify the real branch earlier

first_checks:
- inspect processor-local logs before relying on reconstructed fields or aggregate console output
- compare processor boundary and patch descriptions in the decomposed case when the failure signature mentions patch mismatch, AMI coverage, or processor-local topology trouble
- ask whether the reconstructed field merely shows downstream damage while the processor-local logs identify the first bad rank and interface earlier
- if the failure is localized to a specific processor count or region, inspect that rank's local boundary handling before broad numerics changes
- treat reconstruction as a convenience layer, not as the authoritative first diagnostic surface for parallel-only failures

deeper_checks:
- compare the first failing processor's evidence against neighboring processors to determine whether the issue is local inconsistency or broad instability
- separate true processor-boundary inconsistency from cases where reconstruction only appears cleaner because the serial branch was already marginal
- if coupled, cyclic, or AMI boundaries are involved, inspect whether the processor-local representation is asymmetric even when the reconstructed global patch looks plausible
- verify whether the failure clue disappears after reconstruction because the global field averages or merges away the processor-local discontinuity

likely_fixes:
- debug from processor-local evidence first, then reconstruct only after the failing branch is identified
- adjust decomposition so sensitive interfaces and local hotspots are represented more coherently across processor boundaries
- preserve or constrain sensitive patch groupings where feasible instead of trusting default decomposition blindly
- use reconstruction to verify the post-fix field behavior, not as the first and only truth source

escalation_path:
- if the main clue is a rank-threshold effect, route to `processor-count-sensitive-parallel-failure`
- if the case fails on any parallel launch regardless of count, keep `parallel-only-failure` as the parent branch
- if processor-local evidence leaves ambiguity between hotspot fragmentation and interface semantics, route to `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- if processor-local evidence ultimately points to mesh, BC, or interface semantics, route into those narrower structural nodes rather than staying in the parallel symptom bucket

source_refs:
- official-openfoam-user-guide-parallel
- official-openfoam-decomposePar-guide
- community-openfoam-bugtracker-coupled-patch-parallel-crash
- community-openfoam-bugtracker-cyclicami-single-sided-parallel-crash

confidence: medium
notes:
- This node exists to teach agents that reconstructed global output can hide the first processor-local clue.
- For parallel debugging, processor-local evidence often has higher diagnostic value than the first reconstructed picture.
