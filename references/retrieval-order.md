# Retrieval Order

## Goal
Define a deterministic retrieval order so agents do not wander randomly through the repository.

## A. Case setup tasks
1. Identify the closest `scenario_templates/` file.
2. Read that template’s `recommended_playbooks`.
3. Load `playbooks/case-setup/first-pass-case-setup-checklist.md` unless a more specific playbook is clearly dominant.
4. Pull the minimum required official notes from `knowledge/official/`.
5. Use troubleshooting nodes only if the setup already shows a concrete failure branch.

## B. Troubleshooting tasks
1. Identify the closest `scenario_templates/` file.
2. Read `playbooks/debug-routing/scenario-to-node-routing-v1.md`.
3. Select the best matching playbook.
4. Read `playbooks/debug-routing/playbook-to-node-routing-v1.md`.
5. Load the top 1–3 troubleshooting nodes from `ontology/troubleshooting-graph/nodes/`.
6. Use `knowledge/official/` as the primary evidence layer.
7. Use `knowledge/community/` only as bounded heuristic support.

## C. Case-review tasks
1. Identify the closest `scenario_templates/` file.
2. Use `prompts/case-review.md` as the review frame.
3. Pull the setup checklist.
4. Pull the most relevant official notes.
5. Pull troubleshooting nodes only for clearly visible red-flag branches.

## D. Source-ingestion tasks
1. Use `prompts/source-triage-assistant.md`.
2. Check `references/collection-policy.md`.
3. Record the source in `references/source-index.yaml`.
4. Only then create community source records or distilled notes.

## Hard rule
Do not start from community notes when official guidance already covers the semantics or structure in question.
