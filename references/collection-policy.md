# Collection Policy

## Goal
Collect only high-value OpenFOAM knowledge that improves agent performance in:
- case setup
- solver/model selection
- dictionary review
- troubleshooting divergence, crashes, and nonphysical results

## Inclusion rules
Include sources that are:
- official OpenFOAM documentation, guides, and tutorials
- high-signal community discussions with concrete reasoning or reproducible troubleshooting steps
- relevant to solver choice, numerics, mesh, boundary conditions, initialization, parallelism, and debugging

## Exclusion rules
Exclude sources that are:
- low-quality reposts or SEO blogspam
- vague anecdotal posts without actionable content
- pure source-code deep dives with no setup/debugging value
- duplicate explanations already captured from stronger sources

## Processing rules
For every accepted source:
1. record it in `references/source-index.yaml`
2. assign a trust level
3. summarize key points in source-oriented language
4. create distilled notes only after source capture
5. link all derived notes back to source IDs

## Trust order
1. official docs / official tutorials
2. official issue tracker / official discussions
3. high-quality expert community posts
4. medium-quality community heuristics
5. low-confidence anecdotal tips

## Conflict resolution
- prefer official docs when conflict exists
- retain community workaround notes only if clearly marked as heuristics
- mark scope/limits when advice is solver- or scenario-specific
