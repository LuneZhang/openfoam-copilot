# Contributing

This repository now treats the runtime contract as an enforced maintenance path, not a best-effort convention.

Use the same update order every time so runtime metadata, authored knowledge, generated views, and consumer-facing surfaces do not drift.

## Runtime update order

Follow this order when a change touches runtime-visible content:

1. Update the hand-authored source of truth.
2. Update canonical runtime metadata if IDs, aliases, paths, status, routing, or runtime exposure changed.
3. Run the repository validation commands in the exact order listed here.
4. Regenerate `runtime/generated/` if canonical runtime inputs changed.
5. Confirm the generated-view drift check passes.
6. Only then thin or refresh consumer-facing wrappers that depend on the generated runtime views.

This order matches `runtime/authoring-policy.md` and `runtime/migration-plan.md`:

`registry -> validation -> generation -> consumer-surface refactor -> packaging`

## What to edit first

### Runtime metadata changes

Edit runtime control files first when the change affects identity, routing, aliases, compatibility, or exposure boundaries.

Typical files:

- `runtime/contract.json`
- `runtime/surface.json`
- `runtime/catalog/*.json`
- `runtime/id-policy.md`
- `runtime/authoring-policy.md`
- `runtime/migration-plan.md`

Use this path for changes such as:

- adding or retiring a canonical scenario, playbook, node, prompt, or source ID
- adding aliases or compatibility paths
- changing runtime-visible file paths or status
- changing what belongs in `runtime_public`, `runtime_support`, `authoring_only`, or `project_state`

### Authored knowledge changes

Edit the Markdown knowledge surface first when the OpenFOAM guidance changes but the runtime identity layer does not.

Typical files:

- `scenario_templates/*.md`
- `ontology/troubleshooting-graph/nodes/*.md`
- `knowledge/**/*.md`
- `playbooks/**/*.md`
- `prompts/*.md`
- `references/*.md`
- `references/source-index.yaml`
- `references/citation-map.yaml`

After that, update runtime metadata only if the authored change also changed one of these contract-level facts:

- canonical ID
- alias coverage
- path
- status
- routing target
- runtime surface classification

### Generated views

Do not hand-edit `runtime/generated/*.md`.

Those files are derived from `runtime/contract.json`, `runtime/surface.json`, and `runtime/catalog/*.json`. Regenerate them with the render script whenever canonical runtime inputs change.

## Exact local command order

Run these commands from the repository root in this exact order:

```bash
python3 scripts/validate_contract.py --all
python3 scripts/validate_references.py --all
python3 scripts/validate_routing.py --all
python3 scripts/replay_routing_fixtures.py --all
python3 scripts/render_runtime_views.py --write
python3 scripts/render_runtime_views.py --check
python3 scripts/case_auto_intake.py runtime/fixtures/cases/minimal-valid-case --format json > /tmp/openfoam-copilot-auto-intake.json
python3 -c "import json; from pathlib import Path; data=json.loads(Path('/tmp/openfoam-copilot-auto-intake.json').read_text()); contract=json.loads(Path('runtime/catalog/auto-intake.json').read_text()); assert all(key in data for key in contract['required_fields']); assert all(key in data['structure_inventory'] for key in contract['required_structure_inventory_fields'])"
```

Why this order:

- `validate_contract.py` checks the runtime spine before downstream checks rely on it.
- `validate_references.py` checks source and citation integrity against the canonical runtime/source layer.
- `validate_routing.py` checks that IDs and routing links still resolve.
- `replay_routing_fixtures.py` checks that expected routing behavior still holds.
- `render_runtime_views.py --write` refreshes generated derivatives only after the canonical inputs are already valid.
- `render_runtime_views.py --check` confirms the committed generated files are not stale.
- the auto-intake fixture check confirms the helper output still matches `runtime/catalog/auto-intake.json`.

The CI workflow at `.github/workflows/runtime-contract.yml` runs the non-mutating enforcement subset on `pull_request` and `push`:

```bash
python3 scripts/validate_contract.py --all
python3 scripts/validate_references.py --all
python3 scripts/validate_routing.py --all
python3 scripts/replay_routing_fixtures.py --all
python3 scripts/render_runtime_views.py --check
python3 scripts/case_auto_intake.py runtime/fixtures/cases/minimal-valid-case --format json > /tmp/openfoam-copilot-auto-intake.json && python3 -c "import json; from pathlib import Path; data=json.loads(Path('/tmp/openfoam-copilot-auto-intake.json').read_text()); contract=json.loads(Path('runtime/catalog/auto-intake.json').read_text()); assert all(key in data for key in contract['required_fields']); assert all(key in data['structure_inventory'] for key in contract['required_structure_inventory_fields'])"
```

## Contributor rules

- Keep canonical runtime metadata hand-authored; do not reverse-generate it from Markdown.
- Keep scenario templates, troubleshooting nodes, knowledge notes, playbooks, and prompts hand-authored.
- Keep `project_state` material out of runtime entry surfaces and generated runtime views.
- Add alias coverage before removing or thinning a legacy runtime-visible name.
- Treat `runtime/catalog/sources.json` as canonical for source IDs and aliases; keep reference files aligned with it.
- If a change touches routing, expect both `validate_routing.py` and `replay_routing_fixtures.py` to protect the branch.

## Before opening a pull request

- Make sure the six local commands above pass in order.
- Make sure regenerated files under `runtime/generated/` are committed when canonical runtime inputs changed.
- Make sure consumer-facing wrappers only reflect already-validated canonical or generated runtime facts.
- Make sure no new project-state or planning file was added to the default runtime surface by accident.

For a compact operational version of this process, use `runtime/authoring-checklist.md`.
