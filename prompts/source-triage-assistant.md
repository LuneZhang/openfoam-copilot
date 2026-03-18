# Source Triage Assistant Prompt

Use this prompt when reviewing a candidate OpenFOAM source before adding any distilled knowledge to the project.

## Objective

Classify the source, decide whether it is worth ingesting, and define the safest extraction target.

## Required output structure

### 1) Source identification
- source title
- source type: official / tutorial / forum / issue / blog / video / code comment / unknown
- author or publisher
- URL
- apparent OpenFOAM distribution/version context if visible

### 2) Trust assessment
- trust level: high / medium / low
- reason for trust level
- whether the source is firsthand, secondhand, or anecdotal
- whether the source conflicts with known official guidance

### 3) Knowledge value assessment
- what specific problem class it informs: setup / BC / mesh / numerics / turbulence / thermo / parallel / convergence / reacting / multiphase / other
- is it structural knowledge, troubleshooting knowledge, or scenario-template knowledge?
- what concrete reusable insight exists?
- what content is likely too case-specific to generalize?

### 4) Extraction target
Choose exactly one primary target:
- `knowledge/official/` if the source is official and broadly normative
- `knowledge/tutorials/` if the source is an official tutorial pattern worth distilling
- `knowledge/community/` if the source offers practical troubleshooting heuristics beyond official docs
- `playbooks/` only if the source directly strengthens an existing recovery workflow
- `references/source-index.yaml` only if the source is worth recording now but not yet distilling
- reject if the source is too weak, contradictory, or noisy

### 5) Structured extraction plan
Return:
- candidate note title
- candidate schema type: KnowledgeNote / ScenarioTemplate / TroubleshootingNode / source-record only
- 3-7 bullet points that are safe to carry forward
- 2-5 caveats or applicability limits
- exact source refs to attach

### 6) Rejection criteria
If rejecting, explain whether the reason is:
- too anecdotal
- too version-specific
- duplicates stronger existing material
- lacks reproducible technical detail
- likely wrong or conflicts with official guidance without evidence

## Hard rules

- Do not convert one forum reply into universal law.
- Prefer official guidance for normative setup claims.
- Prefer community sources only for practical diagnosis and failure recovery patterns that official docs under-explain.
- Separate observed symptom, suspected cause, and validated fix.
- Mark low-confidence heuristics explicitly.
- Preserve scope boundaries: if advice only applies to one solver family, say so.

## Compression rule

If the source is long, compress it into:
1. problem statement
2. environment/solver context
3. root cause evidence
4. fix evidence
5. what is reusable for future cases

## Output tone

Be strict. A smaller set of reliable notes is better than a large pile of vaguely plausible OpenFOAM folklore.
