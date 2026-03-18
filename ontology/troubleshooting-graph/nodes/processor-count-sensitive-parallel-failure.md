# Troubleshooting Node — Processor-Count-Sensitive Parallel Failure

id: processor-count-sensitive-parallel-failure
symptom: The case is clean in serial or on a small processor count, but becomes unstable, crashes, or changes behavior only after the processor count is increased.

probable_causes:
- increasing processor count changes the decomposition geometry enough to split a sensitive coupled, cyclic, AMI, or custom interface more aggressively
- some processors end up owning only a pathological subset of a sensitive region when rank count increases
- the case is not generically parallel-bad; it is decomposition-layout-sensitive and only crosses the failure threshold beyond a certain processor count
- per-rank cell clusters become too small or too topologically awkward around the critical interface / hotspot as scaling increases
- processor-local logs reveal the real failure region, but the aggregate run output hides that rank-count sensitivity

first_checks:
- verify whether the case is stable in serial and on at least one lower processor count before treating this as a generic numerics problem
- compare decomposition layouts at the low rank count and the failing higher rank count instead of only comparing solver settings
- inspect whether increased rank count causes a sensitive interface, AMI pair, or local hotspot region to be split more aggressively across processor boundaries
- inspect processor-local logs and boundary files for the failing rank count, not just the reconstructed or aggregate output
- ask whether the symptom appears only after a threshold processor count, because that is itself a routing clue toward decomposition-layout sensitivity

deeper_checks:
- compare `decomposeParDict` method choice and constraints against the geometry of the sensitive region rather than assuming more ranks should behave similarly
- if AMI or coupled patches are involved, inspect whether some processors now see only one side or a badly imbalanced share of the critical pair
- separate rank-count-sensitive decomposition failure from a serial-fragile case that merely fails faster in parallel
- check whether the failing rank count also produces a much smaller cell budget per critical region, making local mesh / BC fragility worse after partitioning

likely_fixes:
- choose a safer decomposition for the failing rank range instead of assuming higher core count is always a free speedup
- constrain sensitive interfaces or regions so they are not fragmented pathologically as processor count increases
- debug the case at the highest clean rank count first, then scale upward deliberately while watching decomposition geometry
- if needed, accept a slightly less balanced decomposition when it preserves sensitive patch/interface integrity better

escalation_path:
- if the case fails at any parallel rank count, route back to `parallel-only-failure`
- if the critical issue is clearly AMI coverage or coupled-patch fragmentation, route into the more specific parallel interface branch rather than staying at the processor-count symptom level
- if it is unclear whether decomposition fragmented a hotspot or merely exposed a pre-existing interface defect, route to `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- if higher processor count only amplifies an already weak serial case, route into the underlying mesh / BC / numerics node instead of blaming decomposition alone

source_refs:
- official-openfoam-user-guide-parallel
- official-openfoam-decomposePar-guide
- community-openfoam-bugtracker-cyclicami-single-sided-parallel-crash
- community-openfoam-bugtracker-coupled-patch-parallel-crash

confidence: medium
notes:
- This node is narrower than `parallel-only-failure`: it is for cases with an observable rank-count threshold.
- More processors can change failure class, not just runtime speed.
