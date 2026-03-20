# Runtime Authoring Policy

## Purpose

This file defines the boundary between hand-authored repository content and generated runtime artifacts.

The goal is simple:

- keep local-files-first consumption intact
- keep Markdown as the main knowledge product
- give validators, generators, and packagers one clear source of truth
- stop routing facts from drifting across multiple consumer surfaces

## Core rules

- OpenFOAM judgment, scenario framing, source weighting, and first-check order stay hand-authored.
- Canonical runtime metadata is also hand-authored. It is the machine-readable control layer for IDs, aliases, paths, and runtime exposure rules.
- Generation is limited to derivative views and packaging outputs that restate canonical runtime facts for a specific consumer surface.
- Generated files never become the only place where a routing rule, alias rule, or runtime boundary is defined.
- Project-state and stage-gate material stay outside the default runtime surface and outside default runtime packaging.

## Hand-authored artifacts

### Canonical runtime control files

These files are edited directly and treated as the source of truth for the runtime spine:

- `runtime/contract.json`
- `runtime/surface.json`
- `runtime/catalog/*.json`
- `runtime/catalog/auto-intake.json`
- `runtime/bundle-manifest.json`
- `runtime/id-policy.md`
- `runtime/authoring-policy.md`
- `runtime/migration-plan.md`

They are not generator output. Validators and generators read them. They should not be reverse-built by scraping Markdown.

### Hand-authored domain content

These artifacts remain primary authored knowledge and routing content:

- `scenario_templates/`
- `ontology/troubleshooting-graph/nodes/`
- `knowledge/official/`
- `knowledge/tutorials/`
- `knowledge/community/`
- `knowledge/distilled/`
- case-facing playbooks under `playbooks/`
- source capture and traceability material under `references/`

These files carry the real OpenFOAM content: scenario shape, troubleshooting order, evidence tiers, applicability limits, and source-backed claims. They are not generated from the runtime catalogs.

### Hand-authored consumer surfaces

These files remain readable task-facing surfaces, even after generation-backed refactors thin them down:

- `AGENT_ENTRY.md`
- `TROUBLESHOOTING_ENTRY.md`
- `CASE_AUTO_INTAKE_SPEC.md`
- `CASE_TRIAGE_PLAYBOOK.md`
- `references/retrieval-order.md`
- `prompts/*.md`
- `skills/openfoam-copilot/SKILL.md`

Their wording stays hand-authored because they are agent-facing instructions. Over time, they should stop carrying independent routing truth and instead point to or consume canonical runtime facts.

## Generated artifacts

Generation is allowed only for derivative outputs such as:

- `runtime/generated/*.md` entry views and retrieval views
- generated skill-bridge fragments or fully rendered bridge views
- generated alias-resolution tables or compatibility summaries
- exported runtime bundle contents under a distribution directory

These artifacts are derived from `runtime/contract.json`, `runtime/surface.json`, `runtime/catalog/*.json`, and other canonical runtime control files.

Generated output may reorganize or summarize runtime facts for a consumer. It must not invent new scenario, node, playbook, prompt, or source meaning.

## Never generate in this architecture

The following stay hand-authored even after the runtime foundation is complete:

- scenario templates
- troubleshooting nodes
- official, tutorial, community, and distilled knowledge notes
- case-facing playbooks
- source records and traceability notes
- prompt wording that shapes agent behavior

This repository is not moving to generator-owned domain content. The runtime layer exists to stabilize access to the authored Markdown, not to replace it.

## How updates should flow

When a routing or runtime fact changes, update it in this order:

1. edit the canonical runtime control file
2. validate the runtime contract against current authored files
3. regenerate derivative runtime views if needed
4. thin or refresh consumer-facing wrappers that read those views

When OpenFOAM knowledge changes, update the authored Markdown directly, then update the catalog or aliases only if identity, routing, or runtime exposure changed.

## Runtime boundary exclusions

The following remain outside the portable runtime surface unless a maintenance task asks for them directly:

- `.sisyphus/`
- stage-gate docs
- progress logs
- validation status reports
- backlog and planning notes

Those files are still hand-authored repository assets, but they are not runtime knowledge dependencies and should not be generated into runtime entry surfaces or shipped as default runtime bundle content.

## Current compatibility note

The present reacting-template compatibility case stays covered exactly as the runtime catalog already defines it:

- canonical scenario ID: `reacting-combustion-flow-generic`
- deprecated alias: `reacting-combustion-generic-template`
- compatibility path alias: `scenario_templates/reacting-combustion-generic-template.md`

That pattern is the model for future migration work: add canonical metadata first, preserve old lookups through aliases, and only then thin legacy consumer references.
