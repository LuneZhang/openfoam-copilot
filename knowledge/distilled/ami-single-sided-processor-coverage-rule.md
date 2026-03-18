# Distilled Rule — Check Whether AMI Pair Coverage Became Single-Sided Per Processor

id: distilled-ami-single-sided-processor-coverage-rule
kind: troubleshooting-rule

rule:
When a cyclicAMI or other AMI-based case works in serial but becomes fragile in parallel, inspect whether decomposition left some processors holding faces from only one side of the AMI pair before broadly retuning numerics.

why_it_matters:
- AMI initialization and matching are processor-local in parallel, so uneven patch ownership can create failures that never appear in the serial code path.
- This failure class often emerges only after rank count increases, which makes decomposition geometry a stronger clue than generic solver settings.
- Inspecting processor boundary files and AMI coverage can shorten debugging time compared with blind timestep or relaxation-factor reductions.

recommended_agent_behavior:
- ask whether the case is stable in serial and whether the failure appears only beyond a certain processor count
- inspect `decomposeParDict` and processor-local `constant/polyMesh/boundary` files
- check whether each processor contains both AMI sides or whether some ranks see only one side of the interface pair
- if the split is pathological, try a safer decomposition that keeps AMI ownership better balanced before changing numerics
- if the interface is geometrically nontrivial, also verify transform/orientation assumptions rather than assuming pure decomposition failure

source_refs:
- community-openfoam-bugtracker-cyclicami-single-sided-parallel-crash
- official-openfoam-user-guide-parallel
- official-openfoam-decomposePar-guide

trust_note:
This is a low-to-medium trust routing rule: official docs justify the decomposition workflow, while the single-sided AMI processor-coverage pattern comes from a historical community issue report.
