# Turbulence Model Basics

id: official-turbulence-model-basics
problem_class: turbulence
confidence: high
source_refs:
- official-openfoam-turbulence-model-overview
- official-openfoam-user-guide-turbulence-properties

## Why this note exists

Turbulence-model selection is one of the most common places where agents overgeneralize. A useful OpenFOAM assistant must distinguish between the role of turbulence modeling in problem framing and the role of numerics in keeping a case stable.

## First principle
Do not choose a turbulence model in isolation. Model choice is constrained by:
- the solver family
- the physics regime
- steady vs transient intent
- required accuracy level
- near-wall treatment expectations
- mesh resolution reality

## Coarse classification
A first-pass agent mental model should separate:
- laminar treatment
- RANS family
- LES family
- other specialized model families where applicable

### Laminar
Use when the case is physically laminar or when the purpose is an intentionally simplified baseline. Do not use laminar just because turbulent setup looks inconvenient.

### RANS
Use when practical engineering closure is needed for turbulent flow without the computational demand of resolved turbulence. This is often the first practical family for many engineering cases.

### LES
Use when resolving larger turbulent structures is part of the objective and the mesh/time-step budget supports it. LES is not just “more accurate RANS”; it comes with stronger grid and transient demands.

## What `turbulenceProperties` means operationally
This dictionary is not cosmetic. It tells the case which turbulence closure path is active and therefore which additional fields, wall treatments, and assumptions become relevant.

A bad turbulence setup can break a case through:
- missing turbulence fields
- inconsistent boundary conditions for turbulence quantities
- mismatch between intended physical regime and closure model
- unrealistic expectations relative to mesh and timestep quality

## Practical selection rules
1. Start from the physics and engineering objective, not from model brand familiarity.
2. If the case is an ordinary engineering turbulent flow and resources are limited, RANS is often the practical baseline.
3. If the case requires transient structure resolution, LES may be justified — but only if the mesh and timestep budget support it.
4. If uncertain, compare against the nearest official tutorial family instead of inventing a model choice from scratch.

## Common failure modes
- enabling turbulence but forgetting required turbulence fields in `0/`
- mixing boundary-condition patterns from different turbulence model families
- choosing a model whose assumptions do not match the mesh resolution or wall treatment strategy
- treating turbulence choice as the first thing to tweak before fixing structural setup or BC issues

## Anti-patterns
- using a turbulence model as a band-aid for bad boundary conditions
- escalating to a more complex turbulence family before the baseline case is stable
- assuming turbulence-model complexity automatically improves correctness

## Recommendation
- Treat turbulence model choice as a problem-framing decision.
- Validate solver family, BC consistency, and mesh reasonableness before blaming turbulence choice for every instability.
- Record turbulence assumptions explicitly in case reviews and playbooks.

## Applicability limits
- Exact model selection depends on the OpenFOAM distribution, problem class, wall treatment, and available mesh quality.
- This note is a first-pass selection guide, not a substitute for model-specific official documentation.
