#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

KEY_LOG_PATTERNS = {
    "floating_point_exception": re.compile(r"floating point exception|sigfpe", re.I),
    "continuity_error": re.compile(r"continuity|time step continuity errors", re.I),
    "courant_issue": re.compile(r"courant", re.I),
    "ami_or_interface": re.compile(r"cyclicami|ami|coupled patch|coupled", re.I),
    "processor_boundary_issue": re.compile(r"processor|processor boundary", re.I),
    "bounding_or_clipping": re.compile(r"bounding|clipping", re.I),
    "fatal_io_or_dictionary": re.compile(r"fatal io|fatal error|keyword .* undefined|cannot find file", re.I),
    "residual_blowup": re.compile(r"diverg|blow|nan|inf", re.I),
}

COMPRESSIBLE_APPS = [
    "rhoPimpleFoam", "rhoSimpleFoam", "sonicFoam", "rhoCentralFoam", "buoyantPimpleFoam", "buoyantSimpleFoam"
]

MULTIPHASE_HINTS = [
    "alpha.", "phaseProperties", "transportProperties", "interFoam", "multiphase", "twoPhase", "phaseFraction"
]

REACTING_HINTS = [
    "chemistryProperties", "reactingFoam", "chemFoam", "combustion", "Y", "species"
]


def read_text(path: Path, limit: int = 200000) -> str:
    try:
        return path.read_text(errors="ignore")[:limit]
    except Exception:
        return ""


def looks_like_case_root(case: Path) -> bool:
    return (case / "0").is_dir() and (case / "constant").is_dir() and (case / "system").is_dir()


def list_zero_fields(case: Path) -> List[str]:
    zero = case / "0"
    if not zero.is_dir():
        return []
    return sorted([p.name for p in zero.iterdir() if p.is_file()])


def key_files(case: Path) -> Dict[str, Optional[str]]:
    candidates = {
        "controlDict": case / "system" / "controlDict",
        "fvSchemes": case / "system" / "fvSchemes",
        "fvSolution": case / "system" / "fvSolution",
        "decomposeParDict": case / "system" / "decomposeParDict",
        "thermophysicalProperties": case / "constant" / "thermophysicalProperties",
        "turbulenceProperties": case / "constant" / "turbulenceProperties",
        "transportProperties": case / "constant" / "transportProperties",
        "chemistryProperties": case / "constant" / "chemistryProperties",
        "combustionProperties": case / "constant" / "combustionProperties",
        "phaseProperties": case / "constant" / "phaseProperties",
    }
    out: Dict[str, Optional[str]] = {}
    for k, p in candidates.items():
        out[k] = str(p) if p.exists() else None
    return out


def get_application(case: Path) -> Optional[str]:
    p = case / "system" / "controlDict"
    if not p.exists():
        return None
    txt = read_text(p)
    m = re.search(r"\bapplication\s+([^;\s]+)\s*;", txt)
    return m.group(1) if m else None


def find_logs(case: Path) -> List[str]:
    logs = []
    for p in sorted(case.iterdir() if case.is_dir() else []):
        if p.is_file() and (p.name.startswith("log") or p.suffix == ".log"):
            logs.append(str(p))
    return logs


def extract_failure_signals(log_paths: List[str]) -> List[str]:
    found = set()
    for lp in log_paths[:5]:
        txt = read_text(Path(lp), limit=400000)
        for key, pattern in KEY_LOG_PATTERNS.items():
            if pattern.search(txt):
                found.add(key)
    return sorted(found)


def detect_parallel_hint(case: Path, log_paths: List[str]) -> str:
    if any(p.name.startswith("processor") and p.is_dir() for p in case.iterdir()):
        return "already_decomposed"
    if (case / "system" / "decomposeParDict").exists():
        return "parallel_capable"
    txt = "\n".join(read_text(Path(p), 50000) for p in log_paths[:3])
    if re.search(r"processor|decomposePar|mpirun", txt, re.I):
        return "parallel_hint_from_logs"
    return "serial_or_unknown"


def pressure_hint(zero_fields: List[str]) -> str:
    has_p = "p" in zero_fields
    has_prgh = "p_rgh" in zero_fields
    if has_p and has_prgh:
        return "both"
    if has_prgh:
        return "p_rgh"
    if has_p:
        return "p"
    return "neither"


def scenario_guess(case: Path, zero_fields: List[str], application: Optional[str], kfiles: Dict[str, Optional[str]]):
    reasons = []
    names = zero_fields + [application or ""] + [Path(v).name for v in kfiles.values() if v]
    joined = " ".join(names)

    if any(f.startswith("alpha.") for f in zero_fields) or kfiles.get("phaseProperties") or re.search(r"interFoam|multiphase|twoPhase", joined, re.I):
        reasons.append("phase fields or multiphase dictionaries detected")
        return "multiphase", reasons

    species_fields = [f for f in zero_fields if re.match(r"^(Y.*|Xi|b|ft)$", f)]
    if kfiles.get("chemistryProperties") or kfiles.get("combustionProperties") or species_fields or re.search(r"reacting|combust", joined, re.I):
        reasons.append("chemistry/combustion dictionaries or species-like fields detected")
        return "reacting", reasons

    if kfiles.get("thermophysicalProperties") or (application in COMPRESSIBLE_APPS if application else False) or "T" in zero_fields:
        reasons.append("thermo dictionary or compressible/thermal solver hints detected")
        return "compressible", reasons

    reasons.append("no stronger multiphase/reacting/compressible signature found")
    return "incompressible_or_unknown", reasons


def recommended_read_order(family: str, parallel_hint: str, signals: List[str], is_case_root: bool) -> List[str]:
    if not is_case_root:
        return []
    order = [
        "TROUBLESHOOTING_ENTRY.md",
        "playbooks/debug-routing/scenario-to-node-routing-v1.md",
    ]
    if parallel_hint != "serial_or_unknown" or any(s in signals for s in ["ami_or_interface", "processor_boundary_issue"]):
        order.append("PARALLEL_TRIAGE_DECISION_TREE.md")
    order.append("playbooks/debug-routing/playbook-to-node-routing-v1.md")
    if family == "compressible":
        order += [
            "scenario_templates/compressible-thermo-flow-generic.md",
            "ontology/troubleshooting-graph/nodes/compressible-steady-startup-too-brittle.md",
            "ontology/troubleshooting-graph/nodes/critical-region-local-mesh-hotspot.md",
        ]
    elif family == "multiphase":
        order += [
            "scenario_templates/multiphase-interface-flow-generic.md",
            "ontology/troubleshooting-graph/nodes/multiphase-interface-initialization-mismatch.md",
            "ontology/troubleshooting-graph/nodes/critical-region-local-mesh-hotspot.md",
        ]
    elif family == "reacting":
        order += [
            "scenario_templates/reacting-combustion-flow-generic.md",
            "ontology/troubleshooting-graph/nodes/reacting-startup-coupling-too-stiff.md",
            "ontology/troubleshooting-graph/nodes/critical-region-local-mesh-hotspot.md",
        ]
    return order


def build_summary(case: Path) -> Dict:
    is_root = looks_like_case_root(case)
    zfields = list_zero_fields(case)
    kfiles = key_files(case)
    app = get_application(case)
    logs = find_logs(case)
    signals = extract_failure_signals(logs)
    family, reasons = scenario_guess(case, zfields, app, kfiles)
    parallel = detect_parallel_hint(case, logs)
    summary = {
        "case_path": str(case.resolve()),
        "case_name": case.name,
        "is_case_root": is_root,
        "application": app,
        "scenario_family_guess": family,
        "scenario_family_reasons": reasons,
        "pressure_variable_hint": pressure_hint(zfields),
        "parallel_hint": parallel,
        "key_files": kfiles,
        "zero_fields": zfields,
        "log_files": logs,
        "failure_signals": signals,
        "recommended_first_read_order": recommended_read_order(family, parallel, signals, is_root),
        "notes": [
            "auto-intake is heuristic and should feed scenario/playbook/node routing rather than replace it",
            "ask the user for extra materials only if routing remains underdetermined after this snapshot",
        ] + (["supplied path is not a recognizable OpenFOAM-style case root yet"] if not is_root else []),
    }
    return summary


def render_markdown(data: Dict) -> str:
    lines = [
        "# OpenFOAM Case Auto-Intake Summary",
        "",
        f"- case_path: `{data['case_path']}`",
        f"- is_case_root: `{data['is_case_root']}`",
        f"- application: `{data['application']}`",
        f"- scenario_family_guess: `{data['scenario_family_guess']}`",
        f"- pressure_variable_hint: `{data['pressure_variable_hint']}`",
        f"- parallel_hint: `{data['parallel_hint']}`",
        "",
        "## Scenario-family reasons",
    ]
    for r in data["scenario_family_reasons"]:
        lines.append(f"- {r}")
    lines += ["", "## Key files"]
    for k, v in data["key_files"].items():
        lines.append(f"- {k}: `{v}`" if v else f"- {k}: missing")
    lines += ["", "## 0/ fields"]
    for f in data["zero_fields"]:
        lines.append(f"- {f}")
    lines += ["", "## Log files"]
    if data["log_files"]:
        for lp in data["log_files"]:
            lines.append(f"- `{lp}`")
    else:
        lines.append("- none found at case root")
    lines += ["", "## Failure signals"]
    if data["failure_signals"]:
        for s in data["failure_signals"]:
            lines.append(f"- {s}")
    else:
        lines.append("- none detected yet")
    lines += ["", "## Recommended first read order"]
    for item in data["recommended_first_read_order"]:
        lines.append(f"- `{item}`")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Auto-collect a first-pass OpenFOAM case snapshot from a case path.")
    ap.add_argument("case_path", help="Path to the case root")
    ap.add_argument("--format", choices=["json", "md"], default="json")
    ap.add_argument("--out", help="Optional output path")
    args = ap.parse_args()

    case = Path(args.case_path)
    data = build_summary(case)
    output = json.dumps(data, indent=2, ensure_ascii=False) if args.format == "json" else render_markdown(data)
    if args.out:
        Path(args.out).write_text(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
