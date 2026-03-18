# Troubleshooting Node — Parallel-Only Failure

id: parallel-only-failure
symptom: The case is sane or at least much more stable in serial, but fails, diverges, or behaves strangely only after decomposition and parallel launch.

probable_causes:
- decomposition strategy unsuitable for the case geometry or processor count
- sensitive coupled / cyclic / custom interfaces split across processor boundaries
- mismatch between decomposition settings and launch setup
- processor-local instability amplifying an already marginal case
- reconstruction / parallel workflow confusion masking the true failure mode

first_checks:
- confirm whether the serial case is structurally valid
- inspect `decomposeParDict`
- confirm processor count and decomposition plan are consistent
- inspect whether decomposition cuts through cyclic / AMI / coupled / custom interfaces
- inspect processor-local logs instead of only aggregated console output

deeper_checks:
- check whether the same symptom exists weakly in serial and is just amplified in parallel
- review whether boundary/patch handling changed materially after decomposition
- inspect whether processor-local evidence shows a boundary/field inconsistency that reconstructed output hides
- separate decomposition issues from underlying numerics instability

likely_fixes:
- fix the serial case first if it is already unstable
- correct decomposition settings and rerun
- change decomposition so sensitive interfaces are not split if feasible
- simplify the startup path before scaling back to parallel

escalation_path:
- if serial remains clean but parallel still fails, branch into decomposition-strategy and environment-specific workflow analysis
- if the failure appears only beyond a higher processor-count threshold, route to `processor-count-sensitive-parallel-failure`
- if processor-local evidence is richer than reconstructed global output, route to `processor-boundary-field-inconsistency`

source_refs:
- official-openfoam-user-guide-parallel
- official-openfoam-decomposePar-guide
- community-openfoam-bugtracker-coupled-patch-parallel-crash
- community-triage-policy-seed

confidence: medium
notes:
- Parallel execution should not be the first place a brand-new fragile case is debugged.
