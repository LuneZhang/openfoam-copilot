# Validation Results

Date: 2026-03-17
Status: validation/calibration stage completed for the current first-pass scope

## Scope of this result set

This file records the first full validation-style audit run after the scenario-expansion first-pass closure.

Current batch covered:
- compressible thermo flow case classes A1-A3 from `VALIDATION_CASE_MATRIX.md`
- multiphase interface flow case classes B1-B3 from `VALIDATION_CASE_MATRIX.md`
- reacting / combustion flow case classes C1-C3 from `VALIDATION_CASE_MATRIX.md`

## Audit method

Used the current repository structure as the evaluation surface:
- scenario template
- scenario-to-node routing
- playbook-to-node routing
- setup / case-review prompt wording
- troubleshooting prompt wording
- parallel triage decision tree when parallel-sensitive behavior is part of the case class

Result labels:
- pass
- weak-pass
- misrouted
- incomplete

---

## Compressible thermo flow

### A1. Structurally wrong thermo/solver pairing
Expected first branches:
- `wrong-solver-family-selection`
- `thermo-chemistry-package-inconsistency`

Observed routing behavior:
- scenario family classification is clear
- setup/checklist path surfaces both expected branches early
- prompt wording strongly prefers structural review before numerics tuning

Result: **pass**

Notes:
- the current system correctly treats this as a setup-class problem, not a generic convergence problem

---

### A2. Structurally plausible but brittle steady startup
Expected first branches:
- `compressible-steady-startup-too-brittle`
- `critical-region-local-mesh-hotspot` if a local region dominates

Observed routing behavior:
- scenario family classification is clear
- scenario routing includes `compressible-steady-startup-too-brittle`
- divergence-recovery routing includes `compressible-steady-startup-too-brittle`
- residual-diagnosis routing now also includes `compressible-steady-startup-too-brittle`
- prompt wording tells the agent to prefer staged or transient startup before generic steady numerics churn

Result: **pass**

Calibration note:
- this case was previously a weak-pass because residual-focused handling stayed too generic
- shallow fix applied: add `compressible-steady-startup-too-brittle` to residual-focused handoff logic

---

### A3. High-gradient local hotspot hidden by globally passable mesh
Expected first branches:
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

Observed routing behavior:
- scenario template and troubleshooting entry both explicitly warn against over-trusting global mesh averages
- scenario routing includes both expected branches
- setup / case-review prompts ask whether one critical local region is weaker than the global summary suggests

Result: **pass**

Notes:
- this remains one of the cleaner parts of the current routing system

---

## Multiphase interface flow

### B1. Wrong interface topology / phase initialization
Expected first branches:
- `multiphase-interface-initialization-mismatch`
- `p-vs-p_rgh-confusion` when pressure framing is also implicated

Observed routing behavior:
- multiphase scenario template explicitly treats interface topology as core structure rather than as a small field-detail issue
- setup checklist and case-review prompt both force pressure convention + interface initialization review before generic timestep retuning
- scenario routing exposes both `p-vs-p_rgh-confusion` and `multiphase-interface-initialization-mismatch` early
- troubleshooting prompt explicitly warns not to treat multiphase cases as only timestep-limited
- residual-diagnosis handoff is now aligned so residual-only wording does not flatten this branch into generic transient advice

Result: **pass**

Notes:
- the current system now protects this case class from the main anti-pattern: jumping straight to CFL/timestep talk while the interface setup itself is still wrong

---

### B2. Interface-region local mesh fragility
Expected first branches:
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

Observed routing behavior:
- multiphase scenario template explicitly names interface-region local fragility, curvature-sensitive regions, and opening/interface weak zones
- troubleshooting entry and case-review prompt both ask whether one critical interface region is much weaker than the global mesh summary suggests
- scenario routing includes both expected branches in sensible order
- mesh-quality playbook is compatible with interface-local reasoning and does not collapse this into only global `checkMesh` averages

Result: **pass**

Notes:
- this branch is structurally coherent and does not currently require a deeper node addition

---

### B3. Serial-clean, parallel-bad interface failure
Expected first branches:
- `parallel-only-failure`
- `processor-boundary-field-inconsistency`
- `decomposition-fragmented-hotspot-vs-interface-semantic-defect`

Observed routing behavior:
- multiphase scenario template explicitly says serial-clean / parallel-bad cases should enter parallel/interface diagnosis before broad numerics retuning
- troubleshooting entry sends serial-clean / parallel-bad behavior into the parallel tree first
- the parallel triage decision tree clearly sequences `parallel-only-failure` → `processor-boundary-field-inconsistency` → `decomposition-fragmented-hotspot-vs-interface-semantic-defect`
- troubleshooting prompt reinforces processor-local evidence over reconstructed-global smoothing and warns against generic CFL advice first

Result: **pass**

Notes:
- this is a strong differentiator relative to a generic CFD assistant because the branch order is explicit rather than implied

---

## Reacting / combustion flow

### C1. Wrong reacting solver/thermo/chemistry structure
Expected first branches:
- `wrong-solver-family-selection`
- `thermo-chemistry-package-inconsistency`

Observed routing behavior:
- reacting scenario routing exposes both expected structural branches early
- setup, case-review, and troubleshooting prompts all say solver-family / thermo / chemistry / species structure must be reviewed before numerics or stiffness talk
- the narrow reacting startup-stiffness node correctly defers to structure-first diagnosis when the reacting branch is not yet structurally coherent

Result: **pass**

Notes:
- this case class now clearly avoids the anti-pattern of calling everything “chemistry stiffness” too early

---

### C2. Structurally plausible but startup coupling too stiff
Expected first branches:
- `reacting-startup-coupling-too-stiff`
- `critical-region-local-mesh-hotspot` if a hotspot dominates

Observed routing behavior:
- reacting scenario template explicitly recommends conservative staged or transient startup before aggressive target solves
- scenario routing includes `reacting-startup-coupling-too-stiff`
- divergence-recovery routing includes `reacting-startup-coupling-too-stiff`
- residual-diagnosis routing now also includes `reacting-startup-coupling-too-stiff`
- hotspot-sensitive escalation remains available rather than flattening all difficult reacting startups into global impossibility

Result: **pass**

Calibration note:
- the main shallow asymmetry found during validation was naming/routing drift between the old alias template (`reacting-combustion-generic-template`) and the current canonical template (`reacting-combustion-flow-generic`)
- shallow fix applied: align playbook references to the canonical reacting template name and keep the old file only as a deprecated compatibility alias

---

### C3. Hotspot-driven reacting instability
Expected first branches:
- `critical-region-local-mesh-hotspot`
- `mesh-quality-driven-instability`

Observed routing behavior:
- reacting scenario template explicitly instructs agents to inspect flame-front / scalar-gradient / heat-release hotspots instead of over-trusting global mesh acceptability
- troubleshooting entry already supports local-hotspot-first reasoning
- scenario routing includes both expected branches
- the reacting startup-stiffness node explicitly tells agents to separate local hotspot dominance from globally impossible reacting physics

Result: **pass**

Notes:
- this case class now routes coherently into local hotspot reasoning rather than generic reacting pessimism

---

## Cross-family asymmetry check

Compared across compressible, multiphase, and reacting families, the current system now behaves much more symmetrically on the main validation dimensions:

### 1. Structure-first protection
Status: **good**
- all three families now explicitly protect setup-class failures from premature numerics tuning

### 2. Startup-stiffness branch availability
Status: **good after shallow calibration**
- compressible and reacting startup-stiffness branches are now present in both divergence-oriented and residual-oriented routing
- multiphase keeps its structure-first protection through interface-initialization logic rather than an unnecessary clone of the startup-stiffness branch

### 3. Local-hotspot sensitivity
Status: **good**
- all three families explicitly warn against trusting global mesh averages when one small region dominates the failure

### 4. Parallel sensitivity
Status: **good for multiphase; acceptable elsewhere**
- multiphase has the clearest parallel-sensitive routing because the interface/decomposition distinction is explicit
- no additional shallow fix was justified for compressible or reacting in this validation batch

### 5. Naming and routing consistency
Status: **improved by shallow fix**
- reacting family previously had avoidable naming drift between a newer canonical template and an older alias template
- current validation pass closes that drift at the playbook/reference level without reopening expansion work

---

## Current summary

### Passed
- A1
- A2
- A3
- B1
- B2
- B3
- C1
- C2
- C3

### Weak-pass
- none

### Misrouted
- none

### Incomplete
- none

## Fixes applied from this batch

1. residual-routing calibration
- added family-specific startup/structure handoff coverage in `playbooks/residual-diagnosis/residual-diagnosis-v1.md`
- this closes the earlier compressible A2 weak-pass and keeps residual-focused routing from flattening multiphase/reacting branches

2. reacting-family naming cleanup
- aligned playbook references from `reacting-combustion-generic-template` to `reacting-combustion-flow-generic`
- updated `scenario_templates/README.md` to the canonical reacting template name
- retained the old reacting template file as a deprecated compatibility alias and synced its branch list so it no longer undermines routing symmetry

## Validation-stage conclusion

For the current first-pass repository scope, the validation/calibration stage is **complete**.

What this means:
- the three target scenario families now pass the representative validation matrix
- the applied fixes were shallow and directly justified by observed routing asymmetries
- there is no current evidence forcing fresh first-pass expansion or new node creation before the next stage

What remains intentionally deferred:
- deeper second-pass sub-branch specialization inside each scenario family
- future replay against real external case logs beyond the current validation matrix
- any broader evidence expansion not directly required by a validation miss
