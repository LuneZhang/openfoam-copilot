# Traceability Rules

## Goal
Keep every important recommendation traceable back to a source layer.

## Rules
1. Every scenario template should cite the source IDs that justify its baseline framing.
2. Every troubleshooting node should cite the official/community records that justify its branch logic.
3. Every playbook should either cite source IDs directly or route explicitly to nodes that do.
4. Prompts may be procedural, but whenever they encode domain-specific rules they should be backed by the knowledge layers they orchestrate.
5. Community heuristics must never appear without trust-level context.

## Preferred evidence order
1. official docs / official tutorials
2. official issue/discussion material when needed
3. medium-trust community sources
4. low-trust community sources only as explicitly labeled corroboration

## Anti-patterns
- citing a node without citing its source IDs
- copying advice from community into a playbook without preserving trust-level context
- letting templates or prompts drift away from the underlying source map

## Maintenance rule
When adding a new node, template, or playbook:
- update `references/citation-map.yaml`
- ensure source IDs exist in `references/source-index.yaml`
- prefer adding one clean mapping now rather than a large cleanup later
