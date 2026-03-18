# Distilled Rule — Check Whether Decomposition Cut a Sensitive Interface

id: distilled-parallel-sensitive-interface-decomposition-rule
kind: troubleshooting-rule

rule:
When a case is acceptable in serial but fails only in parallel, first test whether decomposition cut through a coupled, cyclic, AMI, or custom boundary/interface before broadly changing numerics.

why_it_matters:
- some failure modes are introduced by processor-boundary handling rather than the underlying serial physics setup
- interface-sensitive crashes often appear only after decomposition, so serial success alone does not clear the parallel workflow
- decomposition-focused checks can resolve the issue faster than generic relaxation/timestep reductions

recommended_agent_behavior:
- ask whether the case is reproducibly clean in serial
- inspect `decomposeParDict` and the chosen decomposition method / processor count
- check whether sensitive interfaces were split across processor boundaries
- read processor-local logs for patch-area, topology, or processor-boundary mismatch clues
- if needed, try a safer decomposition or keep the problematic interface on one processor before retuning numerics

source_refs:
- community-openfoam-bugtracker-coupled-patch-parallel-crash
- official-openfoam-user-guide-parallel
- official-openfoam-decomposePar-guide

trust_note:
This rule is a low-to-medium trust routing heuristic: official docs support the decomposition workflow, while the parallel-only interface failure pattern is corroborated by community issue reports.
