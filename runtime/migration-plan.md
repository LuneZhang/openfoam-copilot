# Runtime Migration Plan

## Goal

Move the repository onto a portable runtime foundation without replacing authored Markdown, without moving files, and without a flag-day cutover.

The stable migration sequence is:

`registry -> validation -> generation -> consumer-surface refactor -> packaging`

That order is required because each later stage depends on a clean, canonical runtime spine from the earlier one.

## Guardrails

- Keep full-repo, local-files-first consumption as the default path throughout the rollout.
- Treat authored Markdown as the primary knowledge surface throughout the rollout.
- Make each phase additive first. Thin or retire legacy surfaces only after alias coverage and passing validation exist.
- Do not move or rename runtime-visible content without same-change compatibility coverage.
- Keep project-state files outside default runtime retrieval and outside runtime packaging.

## Phase 1, Registry stabilization

Scope:

- treat `runtime/contract.json`, `runtime/surface.json`, and `runtime/catalog/*.json` as the canonical runtime spine
- keep `runtime/id-policy.md`, `runtime/authoring-policy.md`, and this plan as the written rules around that spine
- make every runtime-visible scenario, playbook, node, prompt, and source resolve to one canonical registry entry

Required behavior:

- add aliases, deprecated aliases, and path aliases before changing any consumer-facing wording that depends on them
- preserve current runtime-visible paths while catalogs are still becoming authoritative
- keep `reacting-combustion-flow-generic` canonical and keep `reacting-combustion-generic-template` as compatibility coverage, not a second canonical object

Exit condition:

- the runtime catalog can describe the current repository shape without breaking existing entry files or authored content paths

## Phase 2, Validation against current files

Scope:

- add contract, reference, routing, and replay validation against the repository as it exists
- validate catalogs against real file paths, source refs, aliases, and runtime-surface boundaries before any generated consumer view becomes authoritative

Required behavior:

- fail on missing keys, unresolved paths, dangling aliases, surface leakage, and routing drift
- check authored content in place rather than rewriting it
- prove that the runtime spine matches the current hand-authored repository before generation starts

Exit condition:

- validation passes on the full repository and catches the known failure classes the plan names

## Phase 3, Generation of derivative runtime views

Scope:

- generate only derivative entry, routing, retrieval, and bridge views
- keep those outputs under a generated runtime surface such as `runtime/generated/`

Required behavior:

- generate from the canonical runtime files, not from ad hoc scraping of consumer docs
- treat generated views as read-only derivatives
- compare generated output for drift and fail when it no longer matches canonical metadata
- keep generated content free of project-state dependencies

Exit condition:

- generated runtime views are reproducible, readable, and trace back cleanly to the canonical runtime spine

## Phase 4, Consumer-surface refactor

Scope:

- thin `AGENT_ENTRY.md`, `TROUBLESHOOTING_ENTRY.md`, `references/retrieval-order.md`, `prompts/*.md`, and `skills/openfoam-copilot/SKILL.md`
- keep task-shaped wording in those files, but stop using them as separate routing truth stores

Required behavior:

- current entrypoint paths remain valid during the refactor
- routing facts, alias rules, and runtime exposure facts come from the canonical runtime layer and its generated views
- legacy wording may remain as wrapper text, installation instructions, or surface-specific guidance, but not as a competing source of IDs or branch logic

Exit condition:

- the current consumer-facing files still work from their existing paths, but factual routing drift is reduced to one canonical source

## Phase 5, Packaging

Scope:

- export a minimal runtime bundle only after registry, validation, generation, and consumer-surface refactor are stable
- keep the full repository as the default local runtime while adding packaging as a portable subset option

Required behavior:

- bundle the contract, surface definition, canonical catalogs, generated views, required authored runtime content, and bridge template material
- exclude `project_state` content by default
- do not promote deprecated files as primary bundle entrypoints

Exit condition:

- a portable runtime bundle can be exported without losing the same local-files-first reading order that works in the full repository

## Alias and deprecation coverage

Every breaking-looking change must follow this order:

1. add the canonical registry entry
2. add alias and path compatibility coverage
3. validate current authored references against that coverage
4. update generated views and consumer wrappers
5. retire legacy references only after default runtime paths no longer depend on them

Rules:

- resolve aliases before routing, validation, generation, and packaging
- prefer deprecating aliases or compatibility paths before deprecating canonical IDs
- do not remove a legacy runtime-visible name in the same step that first introduces the canonical replacement
- keep compatibility until validators, replay fixtures, and default runtime surfaces are all clean

## Rollback behavior

Rollback is phase-local, not a one-shot repository reset.

If a phase regresses, use the last passing phase output and stop promotion to the next phase.

Specific rollback rules:

- registry rollback: keep the last passing catalog and retain alias coverage, do not push unstable IDs into validators or generators
- validation rollback: keep current authored surfaces as primary and fix the validator or metadata before generation continues
- generation rollback: keep generated views out of promoted use and keep current hand-authored entry surfaces active while drift is fixed
- consumer-surface rollback: revert thin-wrapper changes without removing the validated runtime spine underneath them
- packaging rollback: ship no new bundle and continue supporting full-repo local consumption as the default fallback

Rollback must never delete authored domain content or remove compatibility aliases as part of the same recovery step that exposes a regression.

## Wave 4 combustion alignment

Wave 4 stays on top of the runtime foundation. It does not bypass it.

That means:

- keep `reacting-combustion-flow-generic` as the active parent and fallback template
- add the five narrow combustion families as additive canonical scenario IDs, not as renames of the generic reacting template
- keep the priority order already defined by the plan: `premixed-combustion-baseline`, `nonpremixed-diffusion-flame`, `buoyant-fire-compartment`, `partially-premixed-recirculating-combustor`, `spray-combustion`
- require source registration, distribution scope, version scope, validation coverage, and replay fixtures for each new family
- require each new combustion node to earn its place with a distinct first-check order, source backing, and fixture coverage

Recommended rollout inside Wave 4:

1. expand runtime registries and combustion policy
2. add hand-authored combustion evidence notes
3. add hand-authored narrow scenario templates
4. add justified hand-authored combustion nodes and routing handoffs
5. add combustion replay fixtures and refresh generated runtime views

The generic reacting template remains available throughout this work as the fallback for cases that are still only classifiable at the broad reacting-family level.

## What this plan avoids

- no flag-day switch from Markdown to generated content
- no rewrite of domain knowledge into opaque machine-owned files
- no packaging-first rewrite that bypasses validation
- no combustion expansion that lands before the runtime foundation can validate, route, and package it safely
