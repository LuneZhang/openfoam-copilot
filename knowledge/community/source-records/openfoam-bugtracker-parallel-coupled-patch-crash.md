# Source Record — OpenFOAM Issue Tracker: Coupled Patch Crash in Parallel

id: community-openfoam-bugtracker-coupled-patch-parallel-crash
source_type: community
source_name: OpenFOAM Issue Tracking / GitLab snippets
url: https://develop.openfoam.com/Development/OpenFOAM-plus/-/issues/538
date: 2018-07-06
trust_level: low
tags:
- community
- parallel
- decomposition
- coupled-patch
- processor-boundary
- troubleshooting
solver_scope:
- general
- cht
- multiphysics
physics_scope:
- general
- thermal

summary: Community issue discussion showing a case that works in serial and in parallel only while a coupled interface stays on one processor, but crashes when decomposition splits directly across that sensitive coupled patch.

key_points:
- A serial-clean case can still fail only after decomposition if the partition cuts through a coupled or otherwise decomposition-sensitive interface.
- Parallel-only failure should trigger inspection of whether cyclic/AMI/custom/coupled boundaries were split across processor patches.
- Processor-local geometry or topology mismatch errors are often the first useful signal; aggregated console output can hide which processor boundary actually failed.
- For this failure class, changing decomposition strategy or constraining sensitive interfaces can be higher value than immediately damping numerics.

applicability:
- serial case is structurally acceptable but crashes only after `decomposePar` + parallel launch
- failures reference processor boundaries, patch-area mismatch, coupled interfaces, or decomposition-sensitive boundary handling
- debugging order needs to distinguish decomposition/interface issues from underlying solver instability

caveats:
- Evidence quality is low because this record is distilled from public issue-tracker snippets rather than a polished tutorial or KB article.
- The issue is interface-specific, so agents should not overgeneralize it into "all parallel failures are decomposition bugs"; unstable serial numerics still remain the default alternative branch.
