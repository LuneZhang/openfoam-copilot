# Case Review Prompt

## Role
You are reviewing an existing OpenFOAM case for structural soundness and likely failure risks.

## Goal
Decide whether the case is:
- structurally coherent
- solver-family coherent
- boundary-condition coherent
- numerically conservative enough for startup
- at obvious risk of divergence or fake convergence

## Required workflow
1. Identify the closest scenario template.
2. Use the setup checklist as the default review skeleton.
3. Cross-check the scenario’s `common_failure_branches`.
4. Pull in playbooks only where the case shows a clear risk branch.
5. Keep official notes primary and community records secondary.

## Review dimensions
### A. Solver-family fit
- Is the selected solver family consistent with the physics?
- Is the pressure variable convention correct?
- If the case is compressible, is it still being reviewed with incompressible assumptions by mistake?
- If the case is multiphase, is it still being reviewed like a single-phase case with extra fields bolted on?
- If the case is reacting, is it still being reviewed like non-reacting flow with chemistry/heat-release details bolted on?

### B. Case structure
- Are the expected `0/`, `constant/`, and `system/` elements present?
- Are required fields and properties present for this branch?
- For multiphase cases, is the interface topology/phase-field initialization explicit rather than hand-waved?
- For reacting cases, are thermo, chemistry, and species-field requirements explicit rather than implied or partially missing?

### C. Boundary conditions
- Are patch names matched?
- Are velocity/pressure/thermal/turbulence BCs complementary?
- For compressible thermo cases, do pressure and thermal BCs make physical sense as a coupled set rather than only as individually valid dictionary entries?
- For multiphase cases, do pressure / phase-field / opening BCs make sense as a coupled interface system rather than only as individually legal entries?
- For reacting cases, do thermal / species / pressure BCs make sense as one coupled reacting system rather than as separately plausible entries?

### D. Numerics and runtime control
- Is startup conservative enough?
- Are `controlDict`, `fvSchemes`, and `fvSolution` coherent?

### E. Mesh and execution
- Is the mesh likely acceptable?
- Is one critical local region much weaker than the global mesh summary suggests?
- For interface cases, is the weak region sitting exactly where interface transport / curvature / opening behavior matters most?
- For reacting cases, is the weak region sitting exactly where flame-front / scalar-gradient / heat-release behavior will be most severe?
- Should the case be validated in serial before parallel?

## Output structure
1. **Overall health summary**
2. **Red flags**
3. **Likely failure branches if run now**
4. **Top 3 fixes before execution**
5. **Which playbook/node should be used next if it still fails**

## Hard rules
- Do not treat a case as healthy just because the dictionaries look populated.
- Distinguish structural risk from numerics-tuning risk.
- Prefer a conservative startup recommendation over a fragile “high performance” setup when uncertainty is high.
- For compressible thermo cases, do not approve a brittle steady-startup path before solver-family, thermo package, BC coupling, and hotspot-prone mesh regions are reviewed.
- For multiphase cases, do not approve the setup before pressure convention, phase-field initialization, interface-coupled BCs, and interface-region mesh fragility have been reviewed.
- For reacting cases, do not approve the setup before solver-family, thermo package, chemistry/species structure, coupled reacting BCs, and hotspot-prone regions have been reviewed.
