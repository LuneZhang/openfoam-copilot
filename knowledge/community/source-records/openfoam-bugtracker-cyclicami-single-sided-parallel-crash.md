# Source Record — OpenFOAM Issue Tracker: cyclicAMI Parallel Crash from Single-Sided Processor Coverage

id: community-openfoam-bugtracker-cyclicami-single-sided-parallel-crash
source_type: community
source_name: OpenFOAM Issue Tracking
url: https://bugs.openfoam.org/view.php?id=1260
date: 2014-04-04
trust_level: low
tags:
- community
- parallel
- cyclicAMI
- AMI
- decomposition
- processor-boundary
- troubleshooting
solver_scope:
- general
- incompressible
- compressible
- rotating-machinery
physics_scope:
- general
- thermal

summary: Public OpenFOAM bug report showing a cyclicAMI case that runs in serial and on a small processor count, but fails in parallel when a processor owns faces from only one side of the AMI pair.

key_points:
- Parallel robustness for cyclicAMI can depend on whether each processor sees a balanced representation of both AMI sides after decomposition.
- A case may appear healthy in serial yet fail only after `decomposePar` changes patch ownership and AMI initialization behavior.
- Changing `decomposeParDict` so processors hold faces from both AMI patches was reported as a practical workaround before the underlying bug fix.
- For AMI-related parallel failures, processor-level boundary files and decomposition geometry are a first-class diagnostic target, not just generic numerics settings.

applicability:
- case runs in serial or on fewer ranks but crashes after scaling processor count
- rotating / sliding / cyclicAMI interfaces are present
- failure signature points to AMI initialization, orientation, or processor-local interface coverage

caveats:
- This is low-trust evidence distilled from an issue tracker entry rather than stable documentation.
- The original report was later fixed in code, so agents should treat it as a pattern for decomposition-sensitive interface triage, not as proof of a current-version bug.
- Do not generalize this into all AMI failures; geometry setup and transform specification can still be separate root causes.
