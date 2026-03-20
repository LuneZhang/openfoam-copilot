#!/usr/bin/env python3

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from validate_contract import (
    DEFAULT_TARGETS,
    REPO_ROOT,
    classify_surface,
    load_json,
    normalize_path,
)


SOURCE_INDEX_PATH = REPO_ROOT / "references" / "source-index.yaml"
CITATION_MAP_PATH = REPO_ROOT / "references" / "citation-map.yaml"
ALLOWED_SOURCE_TYPES = {"official", "tutorial", "community", "internal"}
ALLOWED_STATUSES = {"active", "deprecated", "removed"}
MARKDOWN_VALIDATION_ROOTS = (
    REPO_ROOT / "scenario_templates",
    REPO_ROOT / "ontology" / "troubleshooting-graph" / "nodes",
    REPO_ROOT / "knowledge",
    REPO_ROOT / "playbooks",
    REPO_ROOT / "prompts",
)


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
class SourceRegistry:
    source_path: Path
    canonical_registry_path: str
    citation_audit_path: str
    entries: Dict[str, Dict[str, Any]]
    alias_to_id: Dict[str, str]


def render_report(report: Report) -> None:
    status = "PASS" if report.error_count == 0 else "FAIL"
    print(f"{status} [{report.label}] {report.source_path}")
    for issue in report.issues:
        print(f"  {issue.severity} {issue.location}: {issue.message}")
    if report.warning_count and report.error_count == 0:
        print(f"  warnings: {report.warning_count}")
    print(f"  checks: {report.checks}")


def strip_quotes(value: str) -> str:
    text = value.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    return text


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


def relative_path(path: Path) -> str:
    return normalize_path(str(path.relative_to(REPO_ROOT)))


def read_text(path: Path) -> Tuple[Optional[str], Optional[str]]:
    try:
        return path.read_text(), None
    except FileNotFoundError:
        return None, f"file does not exist: {path}"
    except OSError as exc:
        return None, f"failed to read file: {exc}"


def classify_repo_path(
    path_text: str, surface_data: Dict[str, Any]
) -> Tuple[Optional[str], List[str]]:
    return classify_surface(path_text, surface_data)


def load_surface_data(report: Report) -> Optional[Dict[str, Any]]:
    data, error = load_json(DEFAULT_TARGETS["surface"])
    if error is not None:
        report.error("runtime-surface", error)
        return None
    if not isinstance(data, dict):
        report.error("runtime-surface", "runtime/surface.json must be a JSON object")
        return None
    return data


def resolve_reference(ref: str, registry: SourceRegistry) -> Optional[str]:
    if ref in registry.entries:
        return ref
    return registry.alias_to_id.get(ref)


def validate_reference_list(
    report: Report,
    location: str,
    refs: Sequence[str],
    registry: SourceRegistry,
) -> List[str]:
    resolved: List[str] = []
    seen_local: set[str] = set()
    for index, ref in enumerate(refs):
        item_location = f"{location}[{index}]"
        if not ensure_string(report, ref, item_location):
            continue
        report.check()
        if ref in seen_local:
            report.error(item_location, f"duplicate source ref '{ref}'")
            continue
        seen_local.add(ref)
        canonical = resolve_reference(ref, registry)
        report.check()
        if canonical is None:
            report.error(item_location, f"unknown source ref '{ref}'")
            continue
        if canonical != ref:
            report.warning(
                item_location, f"uses alias '{ref}' for canonical source '{canonical}'"
            )
        resolved.append(canonical)
    return resolved


def parse_source_index(
    path: Path,
) -> Tuple[Optional[Dict[str, Dict[str, str]]], Optional[str]]:
    text, error = read_text(path)
    if error is not None:
        return None, error
    assert text is not None
    records: Dict[str, Dict[str, str]] = {}
    current: Optional[Dict[str, str]] = None
    current_id: Optional[str] = None
    saw_header = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip() == "sources:":
            saw_header = True
            continue
        match_id = re.match(r"^  - id:\s*(.+?)\s*$", line)
        if match_id:
            current_id = strip_quotes(match_id.group(1))
            current = {"id": current_id, "_line": str(lineno)}
            if current_id in records:
                return None, f"duplicate source id '{current_id}' in {path}:{lineno}"
            records[current_id] = current
            continue
        if current is None:
            continue
        match_key = re.match(r"^    ([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
        if match_key:
            key = match_key.group(1)
            current[key] = strip_quotes(match_key.group(2))
    if not saw_header:
        return None, f"missing 'sources:' header in {path}"
    return records, None


def parse_citation_map(
    path: Path,
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    text, error = read_text(path)
    if error is not None:
        return None, error
    assert text is not None
    if "citations:" not in text:
        return None, f"missing 'citations:' header in {path}"
    entries: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    in_source_refs = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        match_target = re.match(r"^  - target:\s*(.+?)\s*$", line)
        if match_target:
            if current is not None:
                entries.append(current)
            current = {
                "target": strip_quotes(match_target.group(1)),
                "source_refs": [],
                "line": lineno,
            }
            in_source_refs = False
            continue
        if current is None:
            continue
        if re.match(r"^    source_refs:\s*$", line):
            in_source_refs = True
            continue
        if in_source_refs:
            match_ref = re.match(r"^      -\s*(.+?)\s*$", line)
            if match_ref:
                current["source_refs"].append(strip_quotes(match_ref.group(1)))
                continue
            if line.strip() == "":
                continue
            if line.startswith("    "):
                in_source_refs = False
            else:
                in_source_refs = False
        if re.match(r"^    [A-Za-z_][A-Za-z0-9_]*:\s*", line):
            continue
    if current is not None:
        entries.append(current)
    return entries, None


def parse_markdown_source_refs(
    path: Path,
) -> Tuple[Optional[List[str]], Optional[str], Optional[int]]:
    text, error = read_text(path)
    if error is not None:
        return None, error, None
    assert text is not None
    lines = text.splitlines()
    blocks: List[Tuple[int, List[str]]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^(\s*)source_refs:\s*$", line)
        if not match:
            continue
        indent = len(match.group(1))
        refs: List[str] = []
        cursor = index + 1
        while cursor < len(lines):
            candidate = lines[cursor]
            if not candidate.strip():
                if refs:
                    break
                cursor += 1
                continue
            candidate_indent = len(candidate) - len(candidate.lstrip(" "))
            item_match = re.match(r"^\s*-\s*(.+?)\s*$", candidate)
            if candidate_indent >= indent and item_match:
                refs.append(strip_quotes(item_match.group(1)))
                cursor += 1
                continue
            break
        blocks.append((index + 1, refs))
    if not blocks:
        return None, None, None
    if len(blocks) > 1:
        return None, f"multiple source_refs blocks found in {path}", None
    line_number, refs = blocks[0]
    return refs, None, line_number


def load_source_registry() -> Tuple[Report, Optional[SourceRegistry]]:
    report = Report("sources-catalog", DEFAULT_TARGETS["sources-catalog"])
    data, error = load_json(DEFAULT_TARGETS["sources-catalog"])
    if error is not None:
        report.error("sources-catalog", error)
        return report, None
    if not ensure_dict(report, data, "sources-catalog"):
        return report, None
    assert isinstance(data, dict)
    if not ensure_required_keys(
        report,
        data,
        "sources-catalog",
        ("catalog_kind", "canonical_registry_path", "citation_audit_path", "items"),
    ):
        return report, None
    if ensure_string(report, data.get("catalog_kind"), "sources-catalog.catalog_kind"):
        report.check()
        if data["catalog_kind"] != "sources":
            report.error("sources-catalog.catalog_kind", "must be 'sources'")
    canonical_registry_path = data.get("canonical_registry_path")
    citation_audit_path = data.get("citation_audit_path")
    if ensure_string(
        report, canonical_registry_path, "sources-catalog.canonical_registry_path"
    ):
        assert isinstance(canonical_registry_path, str)
        report.check()
        if normalize_path(canonical_registry_path) != "references/source-index.yaml":
            report.error(
                "sources-catalog.canonical_registry_path",
                "must point to references/source-index.yaml",
            )
    if ensure_string(
        report, citation_audit_path, "sources-catalog.citation_audit_path"
    ):
        assert isinstance(citation_audit_path, str)
        report.check()
        if normalize_path(citation_audit_path) != "references/citation-map.yaml":
            report.error(
                "sources-catalog.citation_audit_path",
                "must point to references/citation-map.yaml",
            )
    items = data.get("items")
    if not ensure_list(report, items, "sources-catalog.items", non_empty=True):
        return report, None
    assert isinstance(items, list)

    entries: Dict[str, Dict[str, Any]] = {}
    alias_to_id: Dict[str, str] = {}
    for index, item in enumerate(items):
        location = f"sources-catalog.items[{index}]"
        if not ensure_dict(report, item, location):
            continue
        if not ensure_required_keys(
            report,
            item,
            location,
            (
                "id",
                "aliases",
                "path",
                "status",
                "kind",
                "source_type",
                "distribution_scope",
                "version_scope",
            ),
        ):
            continue
        item_id = item.get("id")
        if not ensure_string(report, item_id, f"{location}.id"):
            continue
        report.check()
        if item_id in entries:
            report.error(f"{location}.id", f"duplicate source id '{item_id}'")
            continue
        if ensure_string(report, item.get("status"), f"{location}.status"):
            report.check()
            if item["status"] not in ALLOWED_STATUSES:
                report.error(
                    f"{location}.status",
                    f"must be one of {', '.join(sorted(ALLOWED_STATUSES))}",
                )
        if ensure_string(report, item.get("kind"), f"{location}.kind"):
            report.check()
            if item["kind"] != "source":
                report.error(f"{location}.kind", "must be 'source'")
        if ensure_string(report, item.get("source_type"), f"{location}.source_type"):
            report.check()
            if item["source_type"] not in ALLOWED_SOURCE_TYPES:
                report.error(
                    f"{location}.source_type",
                    f"must be one of {', '.join(sorted(ALLOWED_SOURCE_TYPES))}",
                )
        ensure_string_list(
            report,
            item.get("distribution_scope"),
            f"{location}.distribution_scope",
            non_empty=True,
        )
        ensure_string_list(
            report,
            item.get("version_scope"),
            f"{location}.version_scope",
            non_empty=True,
        )
        if ensure_string(report, item.get("path"), f"{location}.path"):
            path_text = normalize_path(item["path"])
            path_part, fragment = (
                path_text.split("#", 1) if "#" in path_text else (path_text, None)
            )
            report.check()
            if path_part != "references/source-index.yaml":
                report.error(
                    f"{location}.path", "must point into references/source-index.yaml"
                )
            report.check()
            if fragment != item_id:
                report.error(
                    f"{location}.path",
                    f"must use fragment '#{item_id}' to address the source record",
                )
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
                        f"duplicate source alias '{alias}' already assigned to '{previous}'",
                    )
                    continue
                if alias in entries:
                    report.error(
                        f"{location}.aliases[{alias_index}]",
                        f"alias '{alias}' collides with an existing canonical source id",
                    )
                    continue
                alias_to_id[alias] = item_id
        entries[item_id] = item

    registry = SourceRegistry(
        source_path=DEFAULT_TARGETS["sources-catalog"],
        canonical_registry_path=normalize_path(
            str(canonical_registry_path or "references/source-index.yaml")
        ),
        citation_audit_path=normalize_path(
            str(citation_audit_path or "references/citation-map.yaml")
        ),
        entries=entries,
        alias_to_id=alias_to_id,
    )
    return report, registry


def validate_source_index(registry: SourceRegistry) -> Report:
    report = Report("source-index", SOURCE_INDEX_PATH)
    records, error = parse_source_index(SOURCE_INDEX_PATH)
    if error is not None:
        report.error("source-index", error)
        return report
    assert records is not None

    for source_id, record in records.items():
        line = record.get("_line", "?")
        location = f"source-index:{line}"
        report.check()
        if "source_type" not in record:
            report.error(location, f"source '{source_id}' is missing source_type")
            continue
        report.check()
        if record["source_type"] not in ALLOWED_SOURCE_TYPES:
            report.error(
                location,
                f"source '{source_id}' has unsupported source_type '{record['source_type']}'",
            )

    for source_id, entry in registry.entries.items():
        report.check()
        if source_id not in records:
            report.error(
                "source-index.registry-agreement",
                f"canonical source '{source_id}' is missing from references/source-index.yaml",
            )
            continue
        report.check()
        if records[source_id].get("source_type") != entry.get("source_type"):
            report.error(
                "source-index.registry-agreement",
                f"source_type mismatch for '{source_id}': catalog='{entry.get('source_type')}', source-index='{records[source_id].get('source_type')}'",
            )

    for source_id in records:
        report.check()
        if source_id not in registry.entries:
            report.error(
                "source-index.registry-agreement",
                f"references/source-index.yaml contains '{source_id}' but runtime/catalog/sources.json does not",
            )

    return report


def validate_markdown_refs(
    path: Path,
    registry: SourceRegistry,
    *,
    compare_refs: Optional[Sequence[str]] = None,
    category_check: bool,
    label: str,
) -> Report:
    report = Report(label, path)
    refs, error, line_number = parse_markdown_source_refs(path)
    if error is not None:
        report.error("markdown-source-refs", error)
        return report
    if refs is None:
        report.error("markdown-source-refs", f"no source_refs block found in {path}")
        return report
    report.check()
    if not refs:
        report.error("markdown-source-refs", f"empty source_refs block in {path}")
        return report

    if category_check:
        surface_data = load_surface_data(report)
        if surface_data is not None:
            rel = relative_path(path)
            category, matches = classify_repo_path(rel, surface_data)
            report.check()
            if category is None:
                if matches:
                    report.error(
                        "markdown-source-refs.surface",
                        f"{rel} matches multiple surface categories: {', '.join(matches)}",
                    )
                else:
                    report.error(
                        "markdown-source-refs.surface",
                        f"{rel} is not classified by runtime/surface.json",
                    )
            elif category == "project_state":
                report.error(
                    "markdown-source-refs.surface",
                    f"{rel} must not live in project_state when validating runtime references",
                )
            elif category == "authoring_only":
                report.error(
                    "markdown-source-refs.surface",
                    f"{rel} must not be authoring_only when carrying runtime source_refs",
                )

    validate_reference_list(
        report,
        f"markdown-source-refs:{line_number or 1}",
        refs,
        registry,
    )

    if compare_refs is not None:
        report.check()
        if list(refs) != list(compare_refs):
            report.error(
                "markdown-source-refs.citation-map",
                "inline source_refs do not match references/citation-map.yaml for this target",
            )

    return report


def validate_citation_map(registry: SourceRegistry) -> Report:
    report = Report("citation-map", CITATION_MAP_PATH)
    entries, error = parse_citation_map(CITATION_MAP_PATH)
    if error is not None:
        report.error("citation-map", error)
        return report
    assert entries is not None

    surface_data = load_surface_data(report)
    seen_targets: set[str] = set()
    for index, entry in enumerate(entries):
        location = f"citation-map.citations[{index}]"
        target = normalize_path(str(entry.get("target", "")))
        report.check()
        if not target:
            report.error(location, "missing target")
            continue
        report.check()
        if target in seen_targets:
            report.error(location, f"duplicate target '{target}'")
            continue
        seen_targets.add(target)

        target_path = REPO_ROOT / target
        report.check()
        if not target_path.exists():
            report.error(location, f"target file does not exist: {target}")
            continue

        if surface_data is not None:
            category, matches = classify_repo_path(target, surface_data)
            report.check()
            if category is None:
                if matches:
                    report.error(
                        location,
                        f"target matches multiple surface categories: {', '.join(matches)}",
                    )
                else:
                    report.error(
                        location,
                        f"target is not classified by runtime/surface.json: {target}",
                    )
            elif category != "runtime_public":
                report.error(
                    location,
                    f"target must classify as runtime_public, found '{category}'",
                )

        refs = entry.get("source_refs", [])
        report.check()
        if not refs:
            report.error(location, f"target '{target}' has no source_refs")
            continue
        validate_reference_list(report, f"{location}.source_refs", refs, registry)

        if target_path.suffix == ".md":
            inline_refs, inline_error, _ = parse_markdown_source_refs(target_path)
            if inline_error is not None:
                report.error(location, inline_error)
            elif inline_refs is not None:
                report.check()
                if list(inline_refs) != list(refs):
                    report.error(
                        location,
                        f"citation-map source_refs do not match inline source_refs for '{target}'",
                    )

    return report


def validate_runtime_markdown_sources(registry: SourceRegistry) -> Report:
    report = Report("markdown-source-refs", REPO_ROOT)
    surface_data = load_surface_data(report)
    if surface_data is None:
        return report

    for root in MARKDOWN_VALIDATION_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            rel = relative_path(path)
            category, matches = classify_repo_path(rel, surface_data)
            report.check()
            if category is None:
                if matches:
                    report.error(
                        "markdown-source-refs.surface",
                        f"{rel} matches multiple surface categories: {', '.join(matches)}",
                    )
                continue
            if category != "runtime_public":
                continue
            refs, error, line_number = parse_markdown_source_refs(path)
            if error is not None:
                report.error("markdown-source-refs", error)
                continue
            if refs is None:
                continue
            validate_reference_list(report, f"{rel}:{line_number or 1}", refs, registry)

    return report


def print_source_of_truth(registry: SourceRegistry) -> None:
    print("Source of truth:")
    print(f"  canonical source IDs and aliases: {relative_path(registry.source_path)}")
    print(f"  upstream source registry: {registry.canonical_registry_path}")
    print(f"  citation audit map: {registry.citation_audit_path}")


def infer_kind(path: Path) -> Optional[str]:
    normalized = normalize_path(str(path))
    if normalized == normalize_path(str(DEFAULT_TARGETS["sources-catalog"])):
        return "sources-catalog"
    if normalized == normalize_path(str(SOURCE_INDEX_PATH)):
        return "source-index"
    if normalized == normalize_path(str(CITATION_MAP_PATH)):
        return "citation-map"
    if path.suffix == ".md":
        return "markdown-file"
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate source registry, citations, and source_refs."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate source catalog, source index, citation map, and inline source_refs.",
    )
    parser.add_argument("--file", help="Validate a single file or reference artifact.")
    parser.add_argument(
        "--kind",
        choices=("sources-catalog", "source-index", "citation-map", "markdown-file"),
        help="Force the validation kind for --file.",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit non-zero when warnings are present.",
    )
    args = parser.parse_args()
    if args.all and (args.file or args.kind):
        parser.error("--all cannot be combined with --file or --kind")
    if not args.all and not args.file:
        parser.error("choose --all or --file")
    if args.kind and not args.file:
        parser.error("--kind requires --file")
    return args


def validate_single_file(path: Path, kind: str, registry: SourceRegistry) -> Report:
    if kind == "sources-catalog":
        report, _ = load_source_registry()
        return report
    if kind == "source-index":
        return validate_source_index(registry)
    if kind == "citation-map":
        return validate_citation_map(registry)
    return validate_markdown_sources(path, registry)


def validate_markdown_sources(path: Path, registry: SourceRegistry) -> Report:
    return validate_markdown_refs(
        path,
        registry,
        compare_refs=None,
        category_check=False,
        label="markdown-source-refs",
    )


def main() -> int:
    args = parse_args()
    reports: List[Report] = []

    registry_report, registry = load_source_registry()
    reports.append(registry_report)
    if registry is None:
        for report in reports:
            render_report(report)
        print(
            "Summary: validated 1 target(s), 0 source registry available, 1 failed target(s)."
        )
        return 1

    print_source_of_truth(registry)

    if args.all:
        reports.append(validate_source_index(registry))
        reports.append(validate_citation_map(registry))
        reports.append(validate_runtime_markdown_sources(registry))
    else:
        source_path = Path(args.file).expanduser().resolve()
        kind = args.kind or infer_kind(source_path)
        if kind is None:
            report = Report("unknown", source_path)
            report.error("kind", "could not infer file kind; use --kind")
            reports.append(report)
        else:
            reports.append(validate_single_file(source_path, kind, registry))

    for report in reports:
        render_report(report)

    total_checks = sum(report.checks for report in reports)
    total_errors = sum(report.error_count for report in reports)
    total_warnings = sum(report.warning_count for report in reports)
    failed_targets = sum(1 for report in reports if report.error_count > 0)
    print(
        f"Summary: validated {len(reports)} target(s), {total_checks} checks, "
        f"{total_errors} error(s), {total_warnings} warning(s), {failed_targets} failed target(s)."
    )

    if total_errors:
        return 1
    if args.fail_on_warning and total_warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
