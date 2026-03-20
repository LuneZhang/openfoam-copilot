# Runtime ID Policy

This file defines the canonical runtime ID rules for `runtime/catalog/`.

## Scope

- `runtime/catalog/scenarios.json` is the canonical scenario-template registry.
- `runtime/catalog/playbooks.json` is the canonical playbook registry.
- `runtime/catalog/nodes.json` is the canonical troubleshooting-node registry.
- `runtime/catalog/prompts.json` is the canonical prompt registry.
- `runtime/catalog/sources.json` is the canonical source registry.
- Existing authored Markdown remains the primary content surface; the catalogs define stable machine-readable identity, not a second content layer.

## Canonical ID Rules

- Canonical IDs are lowercase kebab-case strings.
- Reuse an already visible runtime ID when one exists in current authored content.
- Scenario canonical IDs come from `scenario_name` when present, not from a newer convenience filename guess.
- Node canonical IDs come from each node file's `id` field.
- Playbook and prompt canonical IDs come from the runtime-visible file stem unless a stronger existing in-file ID is later introduced.
- Source canonical IDs come from `references/source-index.yaml` and must stay identical to the source registry record ID.
- One runtime object gets one canonical ID. Do not create a parallel ID for the same object in another catalog.

## Path Rules

- `path` values are repository-relative.
- For file-backed objects, `path` points to the canonical authored file.
- For source records stored inside `references/source-index.yaml`, `path` uses `references/source-index.yaml#<source-id>` so the file path stays repository-relative while the record stays addressable.
- Compatibility-only alias files may be recorded in `path_aliases`, but they do not create a second canonical object.

## Alias Rules

- `aliases` list runtime-visible legacy IDs that must resolve to the canonical object.
- Aliases are lookup keys only; they are never a second source of truth.
- Preserve current visible IDs when they are already referenced by authored content, validation notes, prompts, or downstream consumers.
- Add an alias instead of renaming a live runtime-visible concept in place.
- The known reacting compatibility case stays canonicalized as `reacting-combustion-flow-generic` with alias `reacting-combustion-generic-template`.

## Deprecation Rules

- Deprecation applies to aliases or compatibility files before it applies to canonical IDs.
- Keep the canonical object `status` as `active` when only a legacy alias is deprecated.
- Mark deprecated compatibility names in `deprecated_aliases` when the canonical object remains active.
- Keep compatibility files only long enough to bridge current consumers; do not expand deprecated branches into new sibling concepts.
- Never remove a runtime-visible legacy ID without first providing alias coverage in the catalog and documenting the migration window.

## Backward Compatibility

- Runtime consumers must resolve aliases to canonical IDs before routing, validation, or generation work.
- Existing authored references may continue using preserved aliases during the compatibility window, but new authored references should use the canonical ID.
- Backward-compatible migration means: add canonical registry entry -> add alias coverage -> update authored references -> retire compatibility file only after no default runtime path depends on it.
- Do not rename existing runtime-visible concepts without explicit alias coverage in the same change.

## Status Expectations

- Allowed statuses for catalog entries are `active`, `deprecated`, and `removed`.
- The current repository state only publishes `active` canonical objects in the registries created by this task.
- Deprecated aliases may exist under an `active` canonical object without requiring a second deprecated entry.

## Source Scope Rules

- `runtime/catalog/sources.json` is the canonical runtime source registry; `references/citation-map.yaml` remains an audit view that maps authored artifacts to source IDs.
- Every source entry must include `distribution_scope` and `version_scope`.
- `distribution_scope` describes the source's visible distribution or publisher context, using the current repository vocabulary: `openfoam-com`, `openfoam-foundation`, `openfoam-plus`, `cfd-direct`, `simscale`, or `repository-internal`.
- `version_scope` records explicit version visibility when present; use `latest`, an explicit published version such as `2212` or `v13`, `unspecified` when the current source record does not pin a version, and `not-applicable` for repository-internal policy material.
- Do not overstate portability. If the source record does not visibly prove a narrower or broader scope, keep the scope conservative.
