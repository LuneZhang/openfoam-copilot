#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from validate_contract import DEFAULT_TARGETS, REPO_ROOT, load_json, normalize_path


FIXTURE_ROOT = REPO_ROOT / "runtime" / "fixtures" / "routing"
FIXTURE_SCHEMA_PATH = FIXTURE_ROOT / "schema.json"
SCENARIO_ROUTING_PATH = (
    REPO_ROOT / "playbooks" / "debug-routing" / "scenario-to-node-routing-v1.md"
)
PLAYBOOK_ROUTING_PATH = (
    REPO_ROOT / "playbooks" / "debug-routing" / "playbook-to-node-routing-v1.md"
)

SECTION_HEADING_RE = re.compile(r"^##\s+\d+\)\s+(.+?)\s*$")
NODE_BULLET_RE = re.compile(r"^-\s+`([^`]+)`\s*$")
TOKEN_RE = re.compile(r"[a-z0-9]+")

FOCUS_PRIORITY = {
    "structural-setup": [
        "premixed-ignition-or-flame-speed-model-mismatch",
        "nonpremixed-mixture-fraction-or-stoichiometric-inlet-mismatch",
        "firefoam-ventilation-radiation-or-hrr-coupling-mismatch",
        "recirculating-combustor-flame-holding-or-backflow-mismatch",
        "spray-injection-evaporation-coupling-startup-fragility",
        "wrong-solver-family-selection",
        "thermo-chemistry-package-inconsistency",
        "multiphase-interface-initialization-mismatch",
        "patch-name-boundary-mismatch",
        "p-vs-p_rgh-confusion",
        "turbulence-field-startup-mismatch",
        "turbulence-field-family-patch-role-mismatch",
    ],
    "startup-stiffness": [
        "spray-injection-evaporation-coupling-startup-fragility",
        "reacting-startup-coupling-too-stiff",
        "compressible-steady-startup-too-brittle",
        "critical-region-local-mesh-hotspot",
        "courant-driven-transient-instability",
        "mesh-quality-driven-instability",
        "steady-state-divergence-overaggressive-numerics",
    ],
    "mesh-hotspot": [
        "critical-region-local-mesh-hotspot",
        "mesh-quality-driven-instability",
        "localized-divergence-hotspot-triage",
        "courant-driven-transient-instability",
        "continuity-error-growth",
    ],
    "interface-initialization": [
        "multiphase-interface-initialization-mismatch",
        "p-vs-p_rgh-confusion",
        "critical-region-local-mesh-hotspot",
        "mesh-quality-driven-instability",
        "courant-driven-transient-instability",
    ],
    "parallel-sensitive": [
        "parallel-only-failure",
        "processor-boundary-field-inconsistency",
        "decomposition-fragmented-hotspot-vs-interface-semantic-defect",
        "processor-count-sensitive-parallel-failure",
        "courant-driven-transient-instability",
    ],
}


@dataclass
class Issue:
    severity: str
    location: str
    message: str


@dataclass
class Report:
    label: str
    source_path: Path
    checks: int = 0
    issues: List[Issue] = field(default_factory=list)

    def check(self) -> None:
        self.checks += 1

    def error(self, location: str, message: str) -> None:
        self.issues.append(Issue("ERROR", location, message))

    def warning(self, location: str, message: str) -> None:
        self.issues.append(Issue("WARNING", location, message))

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "WARNING")


@dataclass
class CatalogRegistry:
    kind_name: str
    source_path: Path
    entries: Dict[str, Dict[str, Any]]
    alias_to_id: Dict[str, str]

    def resolve(self, value: str) -> Optional[str]:
        if value in self.entries:
            return value
        return self.alias_to_id.get(value)

    def active_ids(self) -> List[str]:
        active: List[str] = []
        for item_id, item in self.entries.items():
            if item.get("status") == "active":
                active.append(item_id)
        return active


@dataclass
class FixtureCase:
    source_path: Path
    case_id: str
    suite: str
    matrix_ref: str
    title: str
    scenario_id: str
    playbook_id: str
    focus: str
    tags: List[str]
    expectations: Dict[str, Any]


def render_report(report: Report) -> None:
    status = "PASS" if report.error_count == 0 else "FAIL"
    print(f"{status} [{report.label}] {report.source_path}")
    for issue in report.issues:
        print(f"  {issue.severity} {issue.location}: {issue.message}")
    if report.warning_count and report.error_count == 0:
        print(f"  warnings: {report.warning_count}")
    print(f"  checks: {report.checks}")


def ensure_dict(report: Report, value: Any, location: str) -> bool:
    report.check()
    if isinstance(value, dict):
        return True
    report.error(location, "must be a JSON object")
    return False


def ensure_list(
    report: Report, value: Any, location: str, *, non_empty: bool = False
) -> bool:
    report.check()
    if not isinstance(value, list):
        report.error(location, "must be a JSON array")
        return False
    if non_empty and not value:
        report.error(location, "must not be empty")
        return False
    return True


def ensure_string(
    report: Report, value: Any, location: str, *, non_empty: bool = True
) -> bool:
    report.check()
    if not isinstance(value, str):
        report.error(location, "must be a string")
        return False
    if non_empty and not value.strip():
        report.error(location, "must not be empty")
        return False
    return True


def ensure_string_list(
    report: Report, value: Any, location: str, *, non_empty: bool = False
) -> bool:
    if not ensure_list(report, value, location, non_empty=non_empty):
        return False
    ok = True
    for index, item in enumerate(value):
        if not ensure_string(report, item, f"{location}[{index}]"):
            ok = False
    return ok


def ensure_required_keys(
    report: Report, data: Dict[str, Any], location: str, required_keys: Sequence[str]
) -> bool:
    ok = True
    for key in required_keys:
        report.check()
        if key not in data:
            report.error(location, f"missing required key '{key}'")
            ok = False
    return ok


def read_text(path: Path) -> Tuple[Optional[str], Optional[str]]:
    try:
        return path.read_text(), None
    except FileNotFoundError:
        return None, f"file does not exist: {path}"
    except OSError as exc:
        return None, f"failed to read file: {exc}"


def relative_path(path: Path) -> str:
    return normalize_path(str(path.relative_to(REPO_ROOT)))


def load_catalog_registry(kind_name: str) -> Tuple[Report, Optional[CatalogRegistry]]:
    source_path = DEFAULT_TARGETS[kind_name]
    report = Report(kind_name, source_path)
    data, error = load_json(source_path)
    if error is not None:
        report.error(kind_name, error)
        return report, None
    if not ensure_dict(report, data, kind_name):
        return report, None
    assert isinstance(data, dict)
    if not ensure_required_keys(report, data, kind_name, ("catalog_kind", "items")):
        return report, None
    items = data.get("items")
    if not ensure_list(report, items, f"{kind_name}.items", non_empty=True):
        return report, None
    assert isinstance(items, list)

    entries: Dict[str, Dict[str, Any]] = {}
    alias_to_id: Dict[str, str] = {}
    for index, item in enumerate(items):
        location = f"{kind_name}.items[{index}]"
        if not ensure_dict(report, item, location):
            continue
        if not ensure_required_keys(
            report, item, location, ("id", "aliases", "status")
        ):
            continue
        item_id = item.get("id")
        if not ensure_string(report, item_id, f"{location}.id"):
            continue
        report.check()
        if item_id in entries:
            report.error(f"{location}.id", f"duplicate id '{item_id}'")
            continue
        aliases = item.get("aliases")
        if ensure_string_list(report, aliases, f"{location}.aliases"):
            for alias_index, alias in enumerate(aliases):
                report.check()
                if alias == item_id:
                    report.error(
                        f"{location}.aliases[{alias_index}]",
                        "must not repeat the canonical id",
                    )
                    continue
                previous = alias_to_id.get(alias)
                report.check()
                if previous is not None:
                    report.error(
                        f"{location}.aliases[{alias_index}]",
                        f"duplicate alias '{alias}' already assigned to '{previous}'",
                    )
                    continue
                if alias in entries:
                    report.error(
                        f"{location}.aliases[{alias_index}]",
                        f"alias '{alias}' collides with canonical id '{alias}'",
                    )
                    continue
                alias_to_id[alias] = item_id
        entries[item_id] = item

    return report, CatalogRegistry(kind_name, source_path, entries, alias_to_id)


def validate_fixture_schema(data: Any, source_path: Path) -> Report:
    report = Report("routing-fixture-schema", source_path)
    if not ensure_dict(report, data, "schema"):
        return report
    assert isinstance(data, dict)
    if not ensure_required_keys(
        report,
        data,
        "schema",
        (
            "schema_version",
            "schema_kind",
            "suite_file_kind",
            "suite_field",
            "required_suite_keys",
            "required_case_keys",
            "allowed_focus_values",
            "expectations",
        ),
    ):
        return report
    report.check()
    if not isinstance(data.get("schema_version"), int):
        report.error("schema.schema_version", "must be an integer")
    if ensure_string(report, data.get("schema_kind"), "schema.schema_kind"):
        report.check()
        if data["schema_kind"] != "routing_fixture_schema":
            report.error("schema.schema_kind", "must be 'routing_fixture_schema'")
    ensure_string(report, data.get("suite_file_kind"), "schema.suite_file_kind")
    ensure_string(report, data.get("suite_field"), "schema.suite_field")
    ensure_string_list(
        report,
        data.get("required_suite_keys"),
        "schema.required_suite_keys",
        non_empty=True,
    )
    ensure_string_list(
        report,
        data.get("required_case_keys"),
        "schema.required_case_keys",
        non_empty=True,
    )
    ensure_string_list(
        report,
        data.get("allowed_focus_values"),
        "schema.allowed_focus_values",
        non_empty=True,
    )
    expectations = data.get("expectations")
    if ensure_dict(report, expectations, "schema.expectations"):
        assert isinstance(expectations, dict)
        ensure_required_keys(
            report,
            expectations,
            "schema.expectations",
            ("required_keys", "required_node_window_keys", "minimum_top_n"),
        )
        ensure_string_list(
            report,
            expectations.get("required_keys"),
            "schema.expectations.required_keys",
            non_empty=True,
        )
        ensure_string_list(
            report,
            expectations.get("required_node_window_keys"),
            "schema.expectations.required_node_window_keys",
            non_empty=True,
        )
        report.check()
        if not isinstance(expectations.get("minimum_top_n"), int):
            report.error("schema.expectations.minimum_top_n", "must be an integer")
    return report


def load_fixture_schema() -> Tuple[Report, Optional[Dict[str, Any]]]:
    data, error = load_json(FIXTURE_SCHEMA_PATH)
    if error is not None:
        report = Report("routing-fixture-schema", FIXTURE_SCHEMA_PATH)
        report.error("schema", error)
        return report, None
    report = validate_fixture_schema(data, FIXTURE_SCHEMA_PATH)
    if report.error_count:
        return report, None
    assert isinstance(data, dict)
    return report, data


def discover_fixture_files() -> List[Path]:
    if not FIXTURE_ROOT.exists():
        return []
    return sorted(
        path
        for path in FIXTURE_ROOT.glob("*.json")
        if path.name != FIXTURE_SCHEMA_PATH.name
    )


def tokenize_label(text: str) -> List[str]:
    return [
        token
        for token in TOKEN_RE.findall(text.lower())
        if token not in {"generic", "template", "v1"}
    ]


def resolve_label_to_catalog_id(
    label: str, registry: CatalogRegistry
) -> Tuple[Optional[str], Optional[str]]:
    direct = registry.resolve(label)
    if direct is not None:
        return direct, None
    label_tokens = set(tokenize_label(label))
    if len(label_tokens) < 2:
        return None, f"could not resolve heading '{label}' to a canonical id"

    best_id: Optional[str] = None
    best_score: Optional[Tuple[float, int, float]] = None
    tied_ids: List[str] = []

    for item_id, item in registry.entries.items():
        best_item_score: Optional[Tuple[float, int, float]] = None
        candidate_labels = [item_id] + list(item.get("aliases", []))
        for candidate_label in candidate_labels:
            candidate_tokens = set(tokenize_label(candidate_label))
            if not candidate_tokens:
                continue
            shared = len(label_tokens & candidate_tokens)
            if shared == 0:
                continue
            coverage = shared / float(len(label_tokens))
            precision = shared / float(len(candidate_tokens))
            score = (coverage, shared, precision)
            if best_item_score is None or score > best_item_score:
                best_item_score = score
        if best_item_score is None:
            continue
        if best_score is None or best_item_score > best_score:
            best_id = item_id
            best_score = best_item_score
            tied_ids = [item_id]
        elif best_item_score == best_score:
            tied_ids.append(item_id)

    if best_id is None or best_score is None:
        return None, f"could not resolve heading '{label}' to a canonical id"
    if best_score[0] < 0.5 or best_score[1] < 2:
        return (
            None,
            f"heading '{label}' does not match any canonical id strongly enough",
        )
    if len(set(tied_ids)) > 1:
        return (
            None,
            f"heading '{label}' is ambiguous across ids: {', '.join(sorted(set(tied_ids)))}",
        )
    return best_id, None


def parse_primary_node_sections(
    path: Path, node_heading: str
) -> Tuple[Report, List[Dict[str, Any]]]:
    report = Report(path.stem, path)
    text, error = read_text(path)
    if error is not None:
        report.error("routing-doc", error)
        return report, []
    assert text is not None

    sections: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    capturing = False
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        heading_match = SECTION_HEADING_RE.match(stripped)
        if heading_match:
            if current is not None:
                sections.append(current)
            current = {
                "heading": heading_match.group(1).strip(),
                "line": lineno,
                "nodes": [],
            }
            capturing = False
            continue
        if current is None:
            continue
        if stripped == node_heading:
            capturing = True
            continue
        if not capturing:
            continue
        node_match = NODE_BULLET_RE.match(stripped)
        if node_match:
            current["nodes"].append(node_match.group(1))
            continue
        if not stripped and current["nodes"]:
            capturing = False
    if current is not None:
        sections.append(current)

    report.check()
    if not sections:
        report.error(
            "routing-doc", f"no numbered sections found in {relative_path(path)}"
        )
        return report, []

    for index, section in enumerate(sections):
        location = f"section[{index}]"
        report.check()
        if not section["nodes"]:
            report.error(
                location,
                f"section '{section['heading']}' does not contain a '{node_heading}' block",
            )
    return report, sections


def build_scenario_routing_map(
    scenario_registry: CatalogRegistry, node_registry: CatalogRegistry
) -> Tuple[Report, Dict[str, List[str]]]:
    section_report, sections = parse_primary_node_sections(
        SCENARIO_ROUTING_PATH, "Primary nodes:"
    )
    report = Report("scenario-routing-doc", SCENARIO_ROUTING_PATH)
    report.checks += section_report.checks
    report.issues.extend(section_report.issues)
    if report.error_count:
        return report, {}

    routing_map: Dict[str, List[str]] = {}
    for index, section in enumerate(sections):
        location = f"scenario-routing[{index}]"
        scenario_id, error = resolve_label_to_catalog_id(
            section["heading"], scenario_registry
        )
        report.check()
        if error is not None or scenario_id is None:
            report.error(location, error or "failed to resolve scenario heading")
            continue
        report.check()
        if scenario_id in routing_map:
            report.error(
                location,
                f"duplicate scenario routing section for '{scenario_id}'",
            )
            continue
        resolved_nodes: List[str] = []
        seen_nodes: set[str] = set()
        for node_index, node_id in enumerate(section["nodes"]):
            item_location = f"{location}.nodes[{node_index}]"
            canonical = node_registry.resolve(node_id)
            report.check()
            if canonical is None:
                report.error(item_location, f"unknown node id '{node_id}'")
                continue
            report.check()
            if canonical in seen_nodes:
                report.error(item_location, f"duplicate node id '{canonical}'")
                continue
            seen_nodes.add(canonical)
            resolved_nodes.append(canonical)
        routing_map[scenario_id] = resolved_nodes

    expected_ids = set(scenario_registry.active_ids())
    seen_ids = set(routing_map)
    for missing_id in sorted(expected_ids - seen_ids):
        report.check()
        report.error(
            "scenario-routing.coverage",
            f"active scenario '{missing_id}' is missing from {relative_path(SCENARIO_ROUTING_PATH)}",
        )
    for extra_id in sorted(seen_ids - expected_ids):
        report.check()
        report.error(
            "scenario-routing.coverage",
            f"routing doc resolved unexpected scenario '{extra_id}'",
        )
    return report, routing_map


def build_playbook_routing_map(
    playbook_registry: CatalogRegistry, node_registry: CatalogRegistry
) -> Tuple[Report, Dict[str, List[str]]]:
    section_report, sections = parse_primary_node_sections(
        PLAYBOOK_ROUTING_PATH, "Primary node handoff targets:"
    )
    report = Report("playbook-routing-doc", PLAYBOOK_ROUTING_PATH)
    report.checks += section_report.checks
    report.issues.extend(section_report.issues)
    if report.error_count:
        return report, {}

    routing_map: Dict[str, List[str]] = {}
    for index, section in enumerate(sections):
        location = f"playbook-routing[{index}]"
        playbook_id = playbook_registry.resolve(section["heading"])
        report.check()
        if playbook_id is None:
            report.error(location, f"unknown playbook id '{section['heading']}'")
            continue
        report.check()
        if playbook_id in routing_map:
            report.error(
                location, f"duplicate playbook routing section for '{playbook_id}'"
            )
            continue
        resolved_nodes: List[str] = []
        seen_nodes: set[str] = set()
        for node_index, node_id in enumerate(section["nodes"]):
            item_location = f"{location}.nodes[{node_index}]"
            canonical = node_registry.resolve(node_id)
            report.check()
            if canonical is None:
                report.error(item_location, f"unknown node id '{node_id}'")
                continue
            report.check()
            if canonical in seen_nodes:
                report.error(item_location, f"duplicate node id '{canonical}'")
                continue
            seen_nodes.add(canonical)
            resolved_nodes.append(canonical)
        routing_map[playbook_id] = resolved_nodes

    expected_ids = set()
    for playbook_id, item in playbook_registry.entries.items():
        if item.get("status") != "active":
            continue
        path_text = str(item.get("path", ""))
        if "/debug-routing/" in path_text:
            continue
        expected_ids.add(playbook_id)
    seen_ids = set(routing_map)
    for missing_id in sorted(expected_ids - seen_ids):
        report.check()
        report.error(
            "playbook-routing.coverage",
            f"active playbook '{missing_id}' is missing from {relative_path(PLAYBOOK_ROUTING_PATH)}",
        )
    for extra_id in sorted(seen_ids - expected_ids):
        report.check()
        report.error(
            "playbook-routing.coverage",
            f"routing doc resolved unexpected playbook '{extra_id}'",
        )
    return report, routing_map


def validate_node_window(
    report: Report,
    location: str,
    value: Any,
    node_registry: CatalogRegistry,
    minimum_top_n: int,
) -> bool:
    if not ensure_dict(report, value, location):
        return False
    assert isinstance(value, dict)
    if not ensure_required_keys(report, value, location, ("top_n", "ids")):
        return False
    report.check()
    if not isinstance(value.get("top_n"), int):
        report.error(f"{location}.top_n", "must be an integer")
    else:
        report.check()
        if value["top_n"] < minimum_top_n:
            report.error(
                f"{location}.top_n",
                f"must be >= {minimum_top_n}",
            )
    if ensure_string_list(report, value.get("ids"), f"{location}.ids", non_empty=True):
        for index, node_id in enumerate(value["ids"]):
            report.check()
            if node_registry.resolve(node_id) is None:
                report.error(f"{location}.ids[{index}]", f"unknown node id '{node_id}'")
    return True


def validate_fixture_file(
    path: Path,
    schema: Dict[str, Any],
    scenario_registry: CatalogRegistry,
    playbook_registry: CatalogRegistry,
    node_registry: CatalogRegistry,
) -> Tuple[Report, List[FixtureCase]]:
    report = Report("routing-fixture", path)
    data, error = load_json(path)
    if error is not None:
        report.error("fixture", error)
        return report, []
    if not ensure_dict(report, data, "fixture"):
        return report, []
    assert isinstance(data, dict)

    required_suite_keys = schema.get("required_suite_keys", [])
    if not ensure_required_keys(report, data, "fixture", required_suite_keys):
        return report, []

    report.check()
    if not isinstance(data.get("fixture_schema_version"), int):
        report.error("fixture.fixture_schema_version", "must be an integer")
    else:
        report.check()
        if data["fixture_schema_version"] != schema.get("schema_version"):
            report.error(
                "fixture.fixture_schema_version",
                f"must match schema version {schema.get('schema_version')}",
            )

    if ensure_string(report, data.get("fixture_kind"), "fixture.fixture_kind"):
        report.check()
        if data["fixture_kind"] != schema.get("suite_file_kind"):
            report.error(
                "fixture.fixture_kind",
                f"must be '{schema.get('suite_file_kind')}'",
            )

    suite_name = data.get("suite")
    ensure_string(report, suite_name, "fixture.suite")
    ensure_string(report, data.get("description"), "fixture.description")

    cases = data.get("cases")
    if not ensure_list(report, cases, "fixture.cases", non_empty=True):
        return report, []
    assert isinstance(cases, list)

    allowed_focus_values = set(schema.get("allowed_focus_values", []))
    expectation_schema = schema.get("expectations", {})
    minimum_top_n = int(expectation_schema.get("minimum_top_n", 1))
    required_case_keys = schema.get("required_case_keys", [])
    required_expectation_keys = expectation_schema.get("required_keys", [])

    loaded_cases: List[FixtureCase] = []
    seen_case_ids: set[str] = set()
    for index, item in enumerate(cases):
        location = f"fixture.cases[{index}]"
        case_error_count = report.error_count
        if not ensure_dict(report, item, location):
            continue
        assert isinstance(item, dict)
        if not ensure_required_keys(report, item, location, required_case_keys):
            continue

        case_id = item.get("id")
        if not ensure_string(report, case_id, f"{location}.id"):
            continue
        case_id = str(case_id)
        report.check()
        if case_id in seen_case_ids:
            report.error(f"{location}.id", f"duplicate case id '{case_id}'")
            continue
        seen_case_ids.add(case_id)

        case_suite = item.get("suite")
        if ensure_string(report, case_suite, f"{location}.suite") and isinstance(
            suite_name, str
        ):
            report.check()
            if case_suite != suite_name:
                report.error(
                    f"{location}.suite",
                    f"must match fixture suite '{suite_name}'",
                )

        matrix_ref = item.get("matrix_ref")
        ensure_string(report, matrix_ref, f"{location}.matrix_ref")
        title = item.get("title")
        ensure_string(report, title, f"{location}.title")

        scenario_id = item.get("scenario_id")
        resolved_scenario_id: Optional[str] = None
        if ensure_string(report, scenario_id, f"{location}.scenario_id"):
            resolved_scenario_id = scenario_registry.resolve(str(scenario_id))
            report.check()
            if resolved_scenario_id is None:
                report.error(
                    f"{location}.scenario_id",
                    f"unknown scenario id '{scenario_id}'",
                )

        playbook_id = item.get("playbook_id")
        resolved_playbook_id: Optional[str] = None
        if ensure_string(report, playbook_id, f"{location}.playbook_id"):
            resolved_playbook_id = playbook_registry.resolve(str(playbook_id))
            report.check()
            if resolved_playbook_id is None:
                report.error(
                    f"{location}.playbook_id",
                    f"unknown playbook id '{playbook_id}'",
                )

        focus = item.get("focus")
        if ensure_string(report, focus, f"{location}.focus"):
            report.check()
            if focus not in allowed_focus_values:
                report.error(
                    f"{location}.focus",
                    f"must be one of {', '.join(sorted(allowed_focus_values))}",
                )

        tags = item.get("tags")
        ensure_string_list(report, tags, f"{location}.tags", non_empty=True)

        expectations = item.get("expectations")
        canonical_expectations: Dict[str, Any] = {}
        if ensure_dict(report, expectations, f"{location}.expectations"):
            assert isinstance(expectations, dict)
            if ensure_required_keys(
                report,
                expectations,
                f"{location}.expectations",
                required_expectation_keys,
            ):
                primary_top_n = expectations.get("primary_branch_top_n")
                report.check()
                if not isinstance(primary_top_n, int):
                    report.error(
                        f"{location}.expectations.primary_branch_top_n",
                        "must be an integer",
                    )
                else:
                    report.check()
                    if primary_top_n < minimum_top_n:
                        report.error(
                            f"{location}.expectations.primary_branch_top_n",
                            f"must be >= {minimum_top_n}",
                        )
                if ensure_string_list(
                    report,
                    expectations.get("primary_branch_any_of"),
                    f"{location}.expectations.primary_branch_any_of",
                    non_empty=True,
                ):
                    primary_any_of: List[str] = []
                    for node_index, node_id in enumerate(
                        expectations["primary_branch_any_of"]
                    ):
                        canonical_node_id = node_registry.resolve(node_id)
                        report.check()
                        if canonical_node_id is None:
                            report.error(
                                f"{location}.expectations.primary_branch_any_of[{node_index}]",
                                f"unknown node id '{node_id}'",
                            )
                            continue
                        primary_any_of.append(canonical_node_id)
                    canonical_expectations["primary_branch_any_of"] = primary_any_of
                    canonical_expectations["primary_branch_top_n"] = primary_top_n
                validate_node_window(
                    report,
                    f"{location}.expectations.required_nodes_in_top_n",
                    expectations.get("required_nodes_in_top_n"),
                    node_registry,
                    minimum_top_n,
                )
                required_window = expectations.get("required_nodes_in_top_n", {})
                if isinstance(required_window, dict) and isinstance(
                    required_window.get("ids"), list
                ):
                    canonical_expectations["required_nodes_in_top_n"] = {
                        "top_n": required_window.get("top_n"),
                        "ids": [
                            node_registry.resolve(node_id) or node_id
                            for node_id in required_window["ids"]
                        ],
                    }
                validate_node_window(
                    report,
                    f"{location}.expectations.avoid_nodes_in_top_n",
                    expectations.get("avoid_nodes_in_top_n"),
                    node_registry,
                    minimum_top_n,
                )
                avoid_window = expectations.get("avoid_nodes_in_top_n", {})
                if isinstance(avoid_window, dict) and isinstance(
                    avoid_window.get("ids"), list
                ):
                    canonical_expectations["avoid_nodes_in_top_n"] = {
                        "top_n": avoid_window.get("top_n"),
                        "ids": [
                            node_registry.resolve(node_id) or node_id
                            for node_id in avoid_window["ids"]
                        ],
                    }

        if report.error_count == case_error_count:
            loaded_cases.append(
                FixtureCase(
                    source_path=path,
                    case_id=str(case_id),
                    suite=str(case_suite),
                    matrix_ref=str(matrix_ref),
                    title=str(title),
                    scenario_id=str(resolved_scenario_id),
                    playbook_id=str(resolved_playbook_id),
                    focus=str(focus),
                    tags=list(tags or []),
                    expectations=canonical_expectations,
                )
            )

    return report, loaded_cases


def validate_fixture_collection(cases: Sequence[FixtureCase]) -> Report:
    report = Report("routing-fixture-collection", FIXTURE_ROOT)
    seen_ids: Dict[str, str] = {}
    for case in cases:
        previous = seen_ids.get(case.case_id)
        report.check()
        if previous is not None:
            report.error(
                "fixture-collection.case_ids",
                f"duplicate case id '{case.case_id}' in {previous} and {relative_path(case.source_path)}",
            )
        else:
            seen_ids[case.case_id] = relative_path(case.source_path)
    report.check()
    if not cases:
        report.error("fixture-collection", "no fixture cases were loaded")
    return report


def load_routing_inputs() -> Tuple[
    List[Report],
    Optional[CatalogRegistry],
    Optional[CatalogRegistry],
    Optional[CatalogRegistry],
    Dict[str, List[str]],
    Dict[str, List[str]],
]:
    reports: List[Report] = []
    scenario_report, scenario_registry = load_catalog_registry("scenarios-catalog")
    playbook_report, playbook_registry = load_catalog_registry("playbooks-catalog")
    node_report, node_registry = load_catalog_registry("nodes-catalog")
    reports.extend([scenario_report, playbook_report, node_report])
    if scenario_registry is None or playbook_registry is None or node_registry is None:
        return reports, scenario_registry, playbook_registry, node_registry, {}, {}
    scenario_routing_report, scenario_map = build_scenario_routing_map(
        scenario_registry, node_registry
    )
    playbook_routing_report, playbook_map = build_playbook_routing_map(
        playbook_registry, node_registry
    )
    reports.extend([scenario_routing_report, playbook_routing_report])
    return (
        reports,
        scenario_registry,
        playbook_registry,
        node_registry,
        scenario_map,
        playbook_map,
    )


def load_fixture_cases(
    fixture_paths: Sequence[Path],
    schema: Dict[str, Any],
    scenario_registry: CatalogRegistry,
    playbook_registry: CatalogRegistry,
    node_registry: CatalogRegistry,
) -> Tuple[List[Report], List[FixtureCase]]:
    reports: List[Report] = []
    all_cases: List[FixtureCase] = []
    for path in fixture_paths:
        report, cases = validate_fixture_file(
            path, schema, scenario_registry, playbook_registry, node_registry
        )
        reports.append(report)
        all_cases.extend(cases)
    reports.append(validate_fixture_collection(all_cases))
    return reports, all_cases


def ranked_nodes_for_case(
    case: FixtureCase,
    scenario_map: Dict[str, List[str]],
    playbook_map: Dict[str, List[str]],
) -> List[str]:
    scenario_nodes = scenario_map.get(case.scenario_id, [])
    playbook_nodes = playbook_map.get(case.playbook_id, [])
    focus_positions = {
        node_id: index for index, node_id in enumerate(FOCUS_PRIORITY[case.focus])
    }
    candidates = set(scenario_nodes) | set(playbook_nodes)
    ranked: List[Tuple[int, int, int, int, str]] = []
    for node_id in candidates:
        in_scenario = node_id in scenario_nodes
        in_playbook = node_id in playbook_nodes
        scenario_index = (
            scenario_nodes.index(node_id) + 1
            if in_scenario
            else len(scenario_nodes) + 20
        )
        playbook_index = (
            playbook_nodes.index(node_id) + 1
            if in_playbook
            else len(playbook_nodes) + 20
        )
        focus_bonus = 0
        if node_id in focus_positions and in_scenario:
            focus_bonus = 500 - (focus_positions[node_id] * 25)
        overlap_bonus = 200 if in_scenario and in_playbook else 0
        playbook_bonus = 40 if in_playbook else 0
        scenario_bonus = 20 if in_scenario else 0
        order_bonus = max(0, 30 - min(scenario_index, playbook_index))
        score = (
            focus_bonus + overlap_bonus + playbook_bonus + scenario_bonus + order_bonus
        )
        ranked.append(
            (
                -score,
                min(scenario_index, playbook_index),
                playbook_index,
                scenario_index,
                node_id,
            )
        )
    ranked.sort()
    return [node_id for _, _, _, _, node_id in ranked]


def evaluate_case_expectations(
    case: FixtureCase, ranked_nodes: Sequence[str]
) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    expectations = case.expectations

    primary_top_n = int(expectations["primary_branch_top_n"])
    primary_nodes = list(expectations["primary_branch_any_of"])
    primary_window = list(ranked_nodes[:primary_top_n])
    if not any(node_id in primary_window for node_id in primary_nodes):
        reasons.append(
            "primary branch mismatch: expected one of "
            + ", ".join(primary_nodes)
            + f" in top {primary_top_n}, got "
            + ", ".join(primary_window)
        )

    required_window = expectations["required_nodes_in_top_n"]
    required_top_n = int(required_window["top_n"])
    required_ids = list(required_window["ids"])
    required_actual = list(ranked_nodes[:required_top_n])
    missing_ids = [
        node_id for node_id in required_ids if node_id not in required_actual
    ]
    if missing_ids:
        reasons.append(
            "missing expected nodes in top "
            + str(required_top_n)
            + ": "
            + ", ".join(missing_ids)
            + f"; got {', '.join(required_actual)}"
        )

    avoid_window = expectations["avoid_nodes_in_top_n"]
    avoid_top_n = int(avoid_window["top_n"])
    avoid_ids = list(avoid_window["ids"])
    avoid_actual = list(ranked_nodes[:avoid_top_n])
    present_avoids = [node_id for node_id in avoid_ids if node_id in avoid_actual]
    if present_avoids:
        reasons.append(
            "anti-pattern nodes present in top "
            + str(avoid_top_n)
            + ": "
            + ", ".join(present_avoids)
        )

    return not reasons, reasons
