# Community Source Triage Framework

id: community-source-triage-framework-v1
problem_class: convergence
confidence: medium
source_refs:
- community-triage-policy-seed
- official-openfoam-user-guide-case-structure
- official-openfoam-user-guide-fvSchemes
- official-openfoam-user-guide-fvSolution

## Why this note exists

Community material is where many real OpenFOAM fixes live, but it is also where bad folk wisdom spreads. This framework defines how to admit community troubleshooting knowledge without letting anecdotal advice pollute the backbone.

## Admission rule

A community source is worth distilling only if it contributes at least one of the following:
- a reproducible symptom-to-cause pattern
- a diagnosis workflow that is more concrete than official docs
- a failure signature tied to a specific solver family or model class
- a fix sequence with clear scope boundaries and side effects

If it only says "try smaller timestep" or "change relaxation factors" without context, it is too weak.

## Community note classes

### Class 1 — troubleshooting signal

Good for:
- recurring startup errors
- mesh-related crash signatures
- parallel-only failure patterns
- BC mismatch symptoms recognized by practitioners

Preferred schema target:
- `TroubleshootingNode`

### Class 2 — bounded heuristic

Good for:
- conservative fallback numerics for a named solver family
- known stability-first startup patterns
- recognizable anti-patterns in turbulence or thermo setup

Preferred schema target:
- `KnowledgeNote`

### Class 3 — scenario-specific anecdote

Good for recording in references only when:
- the case is interesting
- but the lesson is not yet general enough for a project note

Preferred target:
- `references/source-index.yaml` with no distilled note yet

## Triage checklist

Before accepting a source, answer:
1. What exact symptom is being discussed?
2. Is the solver family or physics context explicit?
3. Is there evidence beyond opinion?
4. Is the fix structural, BC-related, mesh-related, numerical, or runtime-control-related?
5. Can the claimed fix be phrased with scope limits?
6. Does it align with or sensibly extend official guidance?

## Red flags

Reject or downgrade when you see:
- advice that ignores solver family
- no case context at all
- numerics tweaks presented as universal truth
- pressure variable confusion (`p` vs `p_rgh`) with no buoyancy context
- unstable cases diagnosed without checking mesh or BCs first
- one-off custom-code fixes presented as standard OpenFOAM behavior

## Safe extraction template

When converting a useful community source into a project note, preserve this order:
1. visible symptom
2. likely cause classes
3. first checks
4. deeper checks
5. likely fixes
6. limits and caveats
7. source refs and confidence

## Recommendation

Use community knowledge to enrich troubleshooting order and symptom recognition, not to replace official structural guidance.

## Rationale

- The project must stay traceable and dependable for agent use.
- Community advice is highest value when it sharpens diagnosis, not when it encourages blind parameter thrashing.
- A triage framework keeps future ingestion consistent across many sources.

## Applicability limits

- High-quality community material may still be version-specific.
- Some excellent fixes come from source code issues or maintainer comments and need extra context before distillation.
- Confidence should stay medium or low unless multiple independent sources agree or the fix is strongly backed by official concepts.
