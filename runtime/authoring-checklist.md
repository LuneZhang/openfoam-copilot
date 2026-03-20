# Runtime Authoring Checklist

Use this checklist whenever a change can affect the runtime contract, routing, references, or generated runtime views.

## Edit discipline

- Update hand-authored OpenFOAM content first when the change is domain guidance.
- Update `runtime/contract.json`, `runtime/surface.json`, or `runtime/catalog/*.json` when IDs, aliases, paths, status, routing, or runtime exposure changed.
- Add alias coverage before thinning or retiring a legacy runtime-visible name.
- Never hand-edit `runtime/generated/*.md`.
- Keep project-state files out of runtime entry surfaces and generated runtime views.

## Exact command order

Run from the repository root:

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

## Release gate

- `validate_contract.py` passes before downstream checks.
- `validate_references.py` passes after any source or citation change.
- `validate_routing.py` and `replay_routing_fixtures.py` pass after any routing-affecting change.
- `render_runtime_views.py --write` is run after canonical runtime metadata changes.
- `render_runtime_views.py --check` passes before commit or pull request.
- the auto-intake fixture output stays aligned with `runtime/catalog/auto-intake.json`.

## Update order reminder

Follow the enforced sequence:

`registry -> validation -> generation -> consumer-surface refactor -> packaging`
