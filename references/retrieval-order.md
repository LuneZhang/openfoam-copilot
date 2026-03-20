# Retrieval Order

## Purpose

Use this file as the human wrapper around the generated retrieval order. The runtime routing truth lives in `runtime/generated/retrieval-order.md`, with boundaries defined by `runtime/contract.json` and `runtime/surface.json`.

## Default runtime use

- Start from `runtime/generated/retrieval-order.md`.
- Treat `runtime_public` as the default surface.
- Pull `runtime_support` only when the generated order or task requires contract, helper, source-registry, or skill-bridge detail.
- Do not pull `authoring_only` or `project_state` by default.

## Task-shaped application

### Setup, troubleshooting, and case-review

Follow the task lane in `runtime/generated/retrieval-order.md` or `runtime/generated/agent-entry.md`. This file does not override those generated paths.

### Source triage and traceability

Use this order when the task is about collecting, registering, or auditing sources:
1. `prompts/source-triage-assistant.md`
2. `references/collection-policy.md`
3. `runtime/catalog/sources.json`
4. `references/source-index.yaml`
5. `references/citation-map.yaml`
6. `references/traceability-rules.md`

## Hard rules

- Do not start from community notes when official guidance already covers the semantics or structure in question.
- Treat `runtime/catalog/sources.json` as the canonical source-registry summary and `references/` as the backing traceability layer.
- Keep project-state and validation documents out of default runtime retrieval unless the question is explicitly about repository status.
