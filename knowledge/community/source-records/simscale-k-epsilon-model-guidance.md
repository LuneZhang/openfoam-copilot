# Source Record — SimScale Docs: k-epsilon Model Guidance

id: community-simscale-docs-k-epsilon-guidance
source_type: community
source_name: SimScale Documentation
url: https://www.simscale.com/docs/simulation-setup/global-settings/k-epsilon/
date: unknown
trust_level: medium
tags:
- community
- turbulence
- k-epsilon
- rans
- wall-treatment
- high-Re
solver_scope:
- incompressible
- rans
- external-aero
- general
physics_scope:
- general

summary: Vendor turbulence-model guidance noting that standard k-epsilon is generally more robust in free-shear / free-stream-dominated high-Re settings, but is not the best choice for near-wall or strongly separated situations.

key_points:
- The k-epsilon family is framed as a practical high-Re baseline rather than a universal turbulence default.
- It is described as more suitable for free-stream / free-shear regions than for difficult near-wall behavior.
- Close-wall, strong-separation, or low-y-plus regimes may require a different turbulence-family / wall-treatment strategy.
- A case that copies k-epsilon-style field logic into a wall-sensitive setup can therefore be structurally wrong before numerics tuning begins.

applicability:
- reviewing RANS setup when the chosen turbulence family seems mismatched to wall treatment or geometry
- distinguishing model-family / field-family mismatch from generic divergence
- supporting a troubleshooting node for turbulence-field-family and patch-role inconsistency

caveats:
- This is vendor guidance, not a canonical OpenFOAM model-selection rule.
- It supports branch narrowing, not final model selection by itself.
- Mesh strategy and wall treatment still matter even when the family choice is reasonable.
