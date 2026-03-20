#!/usr/bin/env python3

import argparse
import json
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_STATUSES = {"active", "deprecated", "removed"}
SURFACE_CATEGORIES = (
    "runtime_public",
    "runtime_support",
    "authoring_only",
    "project_state",
)

DEFAULT_TARGETS = {
    "contract": REPO_ROOT / "runtime" / "contract.json",
    "surface": REPO_ROOT / "runtime" / "surface.json",
    "auto-intake-contract": REPO_ROOT / "runtime" / "catalog" / "auto-intake.json",
    "bundle-manifest": REPO_ROOT / "runtime" / "bundle-manifest.json",
    "scenarios-catalog": REPO_ROOT / "runtime" / "catalog" / "scenarios.json",
    "playbooks-catalog": REPO_ROOT / "runtime" / "catalog" / "playbooks.json",
    "nodes-catalog": REPO_ROOT / "runtime" / "catalog" / "nodes.json",
    "prompts-catalog": REPO_ROOT / "runtime" / "catalog" / "prompts.json",
    "sources-catalog": REPO_ROOT / "runtime" / "catalog" / "sources.json",
}

CATALOG_KIND_TO_NAME = {
    "scenarios": "scenarios-catalog",
    "playbooks": "playbooks-catalog",
    "nodes": "nodes-catalog",
    "prompts": "prompts-catalog",
    "sources": "sources-catalog",
}

CATALOG_EXPECTATIONS = {
    "scenarios-catalog": {
        "catalog_kind": "scenarios",
        "item_kind": "scenario_template",
        "path_prefixes": ("scenario_templates/",),
        "surface_category": "runtime_public",
        "generated_prefixes": ("runtime/generated/",),
    },
    "playbooks-catalog": {
        "catalog_kind": "playbooks",
        "item_kind": "playbook",
        "path_prefixes": ("playbooks/",),
        "surface_category": "runtime_public",
        "generated_prefixes": ("runtime/generated/",),
    },
    "nodes-catalog": {
        "catalog_kind": "nodes",
        "item_kind": "troubleshooting_node",
        "path_prefixes": ("ontology/troubleshooting-graph/nodes/",),
        "surface_category": "runtime_public",
        "generated_prefixes": ("runtime/generated/",),
    },
    "prompts-catalog": {
        "catalog_kind": "prompts",
        "item_kind": "prompt",
        "path_prefixes": ("prompts/",),
        "surface_category": "runtime_public",
        "generated_prefixes": ("runtime/generated/",),
    },
    "sources-catalog": {
        "catalog_kind": "sources",
        "item_kind": "source",
        "path_prefixes": ("references/",),
        "surface_category": "runtime_support",
        "generated_prefixes": (),
    },
}

REQUIRED_CONTRACT_KEYS = (
    "consumer_model",
    "runtime_entrypoints",
    "optional_helpers",
    "fallback_behavior",
    "compatibility_policy",
    "runtime_surface_policy",
)

REQUIRED_SURFACE_KEYS = (
    "surface_version",
    "path_match_policy",
    "default_retrieval_policy",
    "runtime_public",
    "runtime_support",
    "authoring_only",
    "project_state",
)

REQUIRED_AUTO_INTAKE_KEYS = (
    "catalog_version",
    "catalog_kind",
    "path_style",
    "helper",
    "fixture_case",
    "required_fields",
    "required_structure_inventory_fields",
    "authoritative_fields",
    "heuristic_fields",
    "supported_values",
    "manual_fallback_inputs",
    "fields",
)

REQUIRED_BUNDLE_MANIFEST_KEYS = (
    "manifest_version",
    "bundle_name",
    "consumer_model",
    "output_manifest",
    "primary_entrypoints",
    "surface_classes_to_copy",
    "runtime_support",
    "exclude_globs",
    "notes",
)

HAND_AUTHORED_RUNTIME_SUPPORT = (
    "runtime/contract.json",
    "runtime/surface.json",
    "runtime/catalog/auto-intake.json",
    "runtime/bundle-manifest.json",
    "runtime/id-policy.md",
    "runtime/authoring-policy.md",
    "runtime/migration-plan.md",
    "runtime/catalog/scenarios.json",
    "runtime/catalog/playbooks.json",
    "runtime/catalog/nodes.json",
    "runtime/catalog/prompts.json",
    "runtime/catalog/sources.json",
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

    @property
    def ok(self) -> bool:
        return self.error_count == 0


def normalize_path(value: str) -> str:
    return value.replace("\\", "/")


def strip_fragment(value: str) -> Tuple[str, Optional[str]]:
    text = normalize_path(value)
    if "#" not in text:
        return text, None
    path_part, fragment = text.split("#", 1)
    return path_part, fragment or None


def strip_trailing_slash(value: str) -> str:
    if value.endswith("/") and value != "/":
        return value[:-1]
    return value


def is_glob_pattern(value: str) -> bool:
    return any(token in value for token in ("*", "?", "["))


def anchor_from_pattern(pattern: str) -> str:
    for marker in ("*", "?", "["):
        if marker in pattern:
            prefix = pattern.split(marker, 1)[0]
            return strip_trailing_slash(prefix)
    return strip_trailing_slash(pattern)


def resolve_repo_relative(repo_relative: str) -> Path:
    path_text, _ = strip_fragment(repo_relative)
    return REPO_ROOT / strip_trailing_slash(path_text)


def path_exists(repo_relative: str) -> bool:
    return resolve_repo_relative(repo_relative).exists()


def matches_surface_pattern(path_text: str, pattern: str) -> bool:
    normalized_path = strip_trailing_slash(normalize_path(path_text))
    normalized_pattern = normalize_path(pattern)
    if not is_glob_pattern(normalized_pattern):
        return normalized_path == strip_trailing_slash(normalized_pattern)
    if fnmatch(normalized_path, strip_trailing_slash(normalized_pattern)):
        return True
    if normalized_pattern.endswith("/**"):
        prefix = strip_trailing_slash(normalized_pattern[:-3])
        return normalized_path == prefix or normalized_path.startswith(prefix + "/")
    return False


def classify_surface(
    path_text: str, surface_data: Dict[str, Any]
) -> Tuple[Optional[str], List[str]]:
    normalized_path = strip_trailing_slash(normalize_path(path_text))
    exact_matches: List[str] = []
    glob_matches: List[Tuple[int, str]] = []
    for category in SURFACE_CATEGORIES:
        for pattern in surface_data.get(category, []):
            if not isinstance(pattern, str):
                continue
            if not matches_surface_pattern(normalized_path, pattern):
                continue
            if is_glob_pattern(pattern):
                specificity = len(anchor_from_pattern(pattern))
                glob_matches.append((specificity, category))
            else:
                exact_matches.append(category)
    if exact_matches:
        unique = sorted(set(exact_matches))
        if len(unique) == 1:
            return unique[0], unique
        return None, unique
    if not glob_matches:
        return None, []
    best_specificity = max(score for score, _ in glob_matches)
    best_categories = sorted(
        {category for score, category in glob_matches if score == best_specificity}
    )
    if len(best_categories) == 1:
        return best_categories[0], best_categories
    return None, best_categories


def load_json(path: Path) -> Tuple[Optional[Any], Optional[str]]:
    try:
        return json.loads(path.read_text()), None
    except FileNotFoundError:
        return None, f"file does not exist: {path}"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    except OSError as exc:
        return None, f"failed to read file: {exc}"


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


def validate_repo_path(
    report: Report,
    location: str,
    repo_relative: Any,
    *,
    expected_categories: Optional[Iterable[str]] = None,
    require_exists: bool = True,
    allow_fragment: bool = False,
    forbid_categories: Optional[Iterable[str]] = None,
) -> Optional[str]:
    if not ensure_string(report, repo_relative, location):
        return None
    text = normalize_path(repo_relative)
    path_text, fragment = strip_fragment(text)
    if Path(path_text).is_absolute():
        report.error(location, "must be repository-relative, not absolute")
        return None
    if fragment and not allow_fragment:
        report.error(location, "must not include a path fragment")
    if allow_fragment and fragment is None and "#" in text:
        report.error(location, "path fragment must not be empty")
    if require_exists:
        report.check()
        if not path_exists(text):
            report.error(location, f"path does not exist: {path_text}")
            return text
    if expected_categories is not None or forbid_categories is not None:
        surface_data, surface_error = load_json(DEFAULT_TARGETS["surface"])
        if surface_error is not None:
            report.error(
                location,
                f"cannot load runtime surface for classification: {surface_error}",
            )
            return text
        if not isinstance(surface_data, dict):
            report.error(
                location,
                "runtime/surface.json must be a JSON object for classification",
            )
            return text
        category, matches = classify_surface(path_text, surface_data)
        report.check()
        if category is None:
            if matches:
                report.error(
                    location,
                    f"matches multiple surface categories: {', '.join(matches)}",
                )
            else:
                report.error(
                    location, f"is not classified by runtime/surface.json: {path_text}"
                )
            return text
        if expected_categories is not None and category not in set(expected_categories):
            report.error(
                location,
                f"must belong to one of {', '.join(expected_categories)}, found '{category}'",
            )
        if forbid_categories is not None and category in set(forbid_categories):
            report.error(location, f"must not belong to '{category}'")
    return text


def validate_contract(data: Any, source_path: Path) -> Report:
    report = Report("contract", source_path)
    if not ensure_dict(report, data, "contract"):
        return report
    if not ensure_required_keys(report, data, "contract", REQUIRED_CONTRACT_KEYS):
        return report

    if ensure_string(report, data.get("consumer_model"), "contract.consumer_model"):
        report.check()
        if data["consumer_model"] != "local-files-first":
            report.error("contract.consumer_model", "must be 'local-files-first'")

    if ensure_string_list(
        report,
        data.get("runtime_entrypoints"),
        "contract.runtime_entrypoints",
        non_empty=True,
    ):
        for index, entry in enumerate(data["runtime_entrypoints"]):
            validate_repo_path(
                report,
                f"contract.runtime_entrypoints[{index}]",
                entry,
                expected_categories=("runtime_public",),
                forbid_categories=("project_state", "authoring_only"),
            )

    if ensure_string_list(
        report, data.get("optional_helpers"), "contract.optional_helpers"
    ):
        for index, helper in enumerate(data["optional_helpers"]):
            validate_repo_path(
                report,
                f"contract.optional_helpers[{index}]",
                helper,
                expected_categories=("runtime_support", "runtime_public"),
                forbid_categories=("project_state",),
            )

    fallback = data.get("fallback_behavior")
    if ensure_dict(report, fallback, "contract.fallback_behavior"):
        ensure_required_keys(
            report,
            fallback,
            "contract.fallback_behavior",
            (
                "default_mode",
                "when_optional_helpers_are_unavailable",
                "minimum_manual_inputs",
            ),
        )
        ensure_string(
            report,
            fallback.get("default_mode"),
            "contract.fallback_behavior.default_mode",
        )
        ensure_string_list(
            report,
            fallback.get("when_optional_helpers_are_unavailable"),
            "contract.fallback_behavior.when_optional_helpers_are_unavailable",
            non_empty=True,
        )
        ensure_string_list(
            report,
            fallback.get("minimum_manual_inputs"),
            "contract.fallback_behavior.minimum_manual_inputs",
            non_empty=True,
        )

    compatibility = data.get("compatibility_policy")
    if ensure_dict(report, compatibility, "contract.compatibility_policy"):
        ensure_required_keys(
            report,
            compatibility,
            "contract.compatibility_policy",
            ("contract_intent", "guarantees", "change_rules"),
        )
        ensure_string(
            report,
            compatibility.get("contract_intent"),
            "contract.compatibility_policy.contract_intent",
        )
        ensure_string_list(
            report,
            compatibility.get("guarantees"),
            "contract.compatibility_policy.guarantees",
            non_empty=True,
        )
        ensure_string_list(
            report,
            compatibility.get("change_rules"),
            "contract.compatibility_policy.change_rules",
            non_empty=True,
        )

    surface_policy = data.get("runtime_surface_policy")
    if ensure_dict(report, surface_policy, "contract.runtime_surface_policy"):
        ensure_required_keys(
            report,
            surface_policy,
            "contract.runtime_surface_policy",
            (
                "default_runtime_dependencies",
                "default_usage_rule",
                "excluded_from_default_runtime_dependencies",
                "exclusion_rule",
            ),
        )
        ensure_string(
            report,
            surface_policy.get("default_usage_rule"),
            "contract.runtime_surface_policy.default_usage_rule",
        )
        ensure_string(
            report,
            surface_policy.get("exclusion_rule"),
            "contract.runtime_surface_policy.exclusion_rule",
        )
        if ensure_string_list(
            report,
            surface_policy.get("default_runtime_dependencies"),
            "contract.runtime_surface_policy.default_runtime_dependencies",
            non_empty=True,
        ):
            for index, entry in enumerate(
                surface_policy["default_runtime_dependencies"]
            ):
                validate_repo_path(
                    report,
                    f"contract.runtime_surface_policy.default_runtime_dependencies[{index}]",
                    entry,
                    expected_categories=("runtime_public", "runtime_support"),
                    forbid_categories=("project_state", "authoring_only"),
                )
        if ensure_string_list(
            report,
            surface_policy.get("excluded_from_default_runtime_dependencies"),
            "contract.runtime_surface_policy.excluded_from_default_runtime_dependencies",
            non_empty=True,
        ):
            for index, entry in enumerate(
                surface_policy["excluded_from_default_runtime_dependencies"]
            ):
                validate_repo_path(
                    report,
                    f"contract.runtime_surface_policy.excluded_from_default_runtime_dependencies[{index}]",
                    entry,
                    expected_categories=("project_state",),
                    require_exists=True,
                )

    return report


def validate_surface(data: Any, source_path: Path) -> Report:
    report = Report("surface", source_path)
    if not ensure_dict(report, data, "surface"):
        return report
    if not ensure_required_keys(report, data, "surface", REQUIRED_SURFACE_KEYS):
        return report

    report.check()
    if not isinstance(data.get("surface_version"), int):
        report.error("surface.surface_version", "must be an integer")

    path_match_policy = data.get("path_match_policy")
    if ensure_dict(report, path_match_policy, "surface.path_match_policy"):
        ensure_required_keys(
            report,
            path_match_policy,
            "surface.path_match_policy",
            ("root", "path_style", "allowed_pattern_types", "precedence"),
        )
        ensure_string(
            report, path_match_policy.get("root"), "surface.path_match_policy.root"
        )
        ensure_string(
            report,
            path_match_policy.get("path_style"),
            "surface.path_match_policy.path_style",
        )
        ensure_string_list(
            report,
            path_match_policy.get("allowed_pattern_types"),
            "surface.path_match_policy.allowed_pattern_types",
            non_empty=True,
        )
        ensure_string_list(
            report,
            path_match_policy.get("precedence"),
            "surface.path_match_policy.precedence",
            non_empty=True,
        )

    default_policy = data.get("default_retrieval_policy")
    if ensure_dict(report, default_policy, "surface.default_retrieval_policy"):
        ensure_required_keys(
            report,
            default_policy,
            "surface.default_retrieval_policy",
            (
                "default_classes",
                "include_runtime_support_when",
                "exclude_by_default",
                "explicit_opt_in_required_for",
                "entry_surfaces",
            ),
        )
        for field_name in (
            "default_classes",
            "exclude_by_default",
            "explicit_opt_in_required_for",
        ):
            if ensure_string_list(
                report,
                default_policy.get(field_name),
                f"surface.default_retrieval_policy.{field_name}",
                non_empty=True,
            ):
                for index, category in enumerate(default_policy[field_name]):
                    report.check()
                    if category not in SURFACE_CATEGORIES:
                        report.error(
                            f"surface.default_retrieval_policy.{field_name}[{index}]",
                            f"unknown surface category '{category}'",
                        )
        ensure_string_list(
            report,
            default_policy.get("include_runtime_support_when"),
            "surface.default_retrieval_policy.include_runtime_support_when",
            non_empty=True,
        )
        if ensure_string_list(
            report,
            default_policy.get("entry_surfaces"),
            "surface.default_retrieval_policy.entry_surfaces",
            non_empty=True,
        ):
            for index, entry in enumerate(default_policy["entry_surfaces"]):
                validate_repo_path(
                    report,
                    f"surface.default_retrieval_policy.entry_surfaces[{index}]",
                    entry,
                    expected_categories=("runtime_public",),
                    forbid_categories=("project_state", "authoring_only"),
                )

    exact_patterns: Dict[str, str] = {}
    for category in SURFACE_CATEGORIES:
        entries = data.get(category)
        if not ensure_string_list(
            report, entries, f"surface.{category}", non_empty=True
        ):
            continue
        for index, pattern in enumerate(entries):
            location = f"surface.{category}[{index}]"
            if is_glob_pattern(pattern):
                anchor = anchor_from_pattern(pattern)
                report.check()
                if not anchor:
                    report.error(
                        location, "glob pattern must include a non-empty path anchor"
                    )
                    continue
                report.check()
                if not (REPO_ROOT / anchor).exists():
                    report.error(location, f"glob anchor does not exist: {anchor}")
            else:
                validate_repo_path(report, location, pattern, require_exists=True)
                previous = exact_patterns.get(pattern)
                report.check()
                if previous is not None and previous != category:
                    report.error(
                        location, f"exact path is already classified under '{previous}'"
                    )
                exact_patterns[pattern] = category

    for runtime_path in HAND_AUTHORED_RUNTIME_SUPPORT:
        category, matches = classify_surface(runtime_path, data)
        report.check()
        if category is None:
            if matches:
                report.error(
                    "surface.runtime_support_boundary",
                    f"{runtime_path} matches multiple categories: {', '.join(matches)}",
                )
            else:
                report.error(
                    "surface.runtime_support_boundary",
                    f"{runtime_path} is not classified by the runtime surface",
                )
        elif category != "runtime_support":
            report.error(
                "surface.runtime_support_boundary",
                f"{runtime_path} must classify as runtime_support, found '{category}'",
            )

    return report


def validate_auto_intake_contract(data: Any, source_path: Path) -> Report:
    report = Report("auto-intake-contract", source_path)
    if not ensure_dict(report, data, "auto-intake-contract"):
        return report
    if not ensure_required_keys(
        report,
        data,
        "auto-intake-contract",
        REQUIRED_AUTO_INTAKE_KEYS,
    ):
        return report

    report.check()
    if not isinstance(data.get("catalog_version"), int):
        report.error("auto-intake-contract.catalog_version", "must be an integer")
    if ensure_string(
        report,
        data.get("catalog_kind"),
        "auto-intake-contract.catalog_kind",
    ):
        report.check()
        if data["catalog_kind"] != "auto_intake_contract":
            report.error(
                "auto-intake-contract.catalog_kind",
                "must be 'auto_intake_contract'",
            )
    if ensure_string(report, data.get("path_style"), "auto-intake-contract.path_style"):
        report.check()
        if data["path_style"] != "repository-relative":
            report.error(
                "auto-intake-contract.path_style",
                "must be 'repository-relative'",
            )

    helper = data.get("helper")
    if ensure_dict(report, helper, "auto-intake-contract.helper"):
        ensure_required_keys(
            report,
            helper,
            "auto-intake-contract.helper",
            ("path", "optional", "mode"),
        )
        validate_repo_path(
            report,
            "auto-intake-contract.helper.path",
            helper.get("path"),
            expected_categories=("runtime_support", "runtime_public"),
            forbid_categories=("project_state",),
        )
        report.check()
        if not isinstance(helper.get("optional"), bool):
            report.error(
                "auto-intake-contract.helper.optional",
                "must be a boolean",
            )
        ensure_string(
            report,
            helper.get("mode"),
            "auto-intake-contract.helper.mode",
        )

    validate_repo_path(
        report,
        "auto-intake-contract.fixture_case",
        data.get("fixture_case"),
        expected_categories=("runtime_support",),
        forbid_categories=("project_state",),
    )

    if (
        ensure_string_list(
            report,
            data.get("required_fields"),
            "auto-intake-contract.required_fields",
            non_empty=True,
        )
        and ensure_string_list(
            report,
            data.get("authoritative_fields"),
            "auto-intake-contract.authoritative_fields",
            non_empty=True,
        )
        and ensure_string_list(
            report,
            data.get("heuristic_fields"),
            "auto-intake-contract.heuristic_fields",
            non_empty=True,
        )
    ):
        required_fields = set(data["required_fields"])
        classified = set(data["authoritative_fields"]) | set(data["heuristic_fields"])
        report.check()
        if required_fields != classified:
            report.error(
                "auto-intake-contract.field_classification",
                "authoritative_fields and heuristic_fields must partition required_fields",
            )

    ensure_string_list(
        report,
        data.get("required_structure_inventory_fields"),
        "auto-intake-contract.required_structure_inventory_fields",
        non_empty=True,
    )
    ensure_string_list(
        report,
        data.get("manual_fallback_inputs"),
        "auto-intake-contract.manual_fallback_inputs",
        non_empty=True,
    )

    supported_values = data.get("supported_values")
    if ensure_dict(report, supported_values, "auto-intake-contract.supported_values"):
        for key in (
            "scenario_family_guess",
            "pressure_variable_hint",
            "parallel_hint",
            "failure_signals",
        ):
            ensure_string_list(
                report,
                supported_values.get(key),
                f"auto-intake-contract.supported_values.{key}",
                non_empty=True,
            )

    fields = data.get("fields")
    if ensure_dict(report, fields, "auto-intake-contract.fields"):
        required_fields = data.get("required_fields", [])
        if isinstance(required_fields, list):
            for field_name in required_fields:
                report.check()
                if field_name not in fields:
                    report.error(
                        "auto-intake-contract.fields",
                        f"missing field description for '{field_name}'",
                    )
                    continue
                descriptor = fields[field_name]
                if not ensure_dict(
                    report,
                    descriptor,
                    f"auto-intake-contract.fields.{field_name}",
                ):
                    continue
                ensure_required_keys(
                    report,
                    descriptor,
                    f"auto-intake-contract.fields.{field_name}",
                    ("type", "required", "classification", "description"),
                )
                report.check()
                if not isinstance(descriptor.get("required"), bool):
                    report.error(
                        f"auto-intake-contract.fields.{field_name}.required",
                        "must be a boolean",
                    )
                ensure_string(
                    report,
                    descriptor.get("classification"),
                    f"auto-intake-contract.fields.{field_name}.classification",
                )
                ensure_string(
                    report,
                    descriptor.get("description"),
                    f"auto-intake-contract.fields.{field_name}.description",
                )

    return report


def validate_bundle_manifest(data: Any, source_path: Path) -> Report:
    report = Report("bundle-manifest", source_path)
    if not ensure_dict(report, data, "bundle-manifest"):
        return report
    if not ensure_required_keys(
        report,
        data,
        "bundle-manifest",
        REQUIRED_BUNDLE_MANIFEST_KEYS,
    ):
        return report

    report.check()
    if not isinstance(data.get("manifest_version"), int):
        report.error("bundle-manifest.manifest_version", "must be an integer")
    ensure_string(report, data.get("bundle_name"), "bundle-manifest.bundle_name")
    if ensure_string(
        report, data.get("consumer_model"), "bundle-manifest.consumer_model"
    ):
        report.check()
        if data["consumer_model"] != "local-files-first":
            report.error(
                "bundle-manifest.consumer_model",
                "must be 'local-files-first'",
            )
    ensure_string(
        report,
        data.get("output_manifest"),
        "bundle-manifest.output_manifest",
    )

    if ensure_string_list(
        report,
        data.get("surface_classes_to_copy"),
        "bundle-manifest.surface_classes_to_copy",
        non_empty=True,
    ):
        for index, name in enumerate(data["surface_classes_to_copy"]):
            report.check()
            if name not in SURFACE_CATEGORIES:
                report.error(
                    f"bundle-manifest.surface_classes_to_copy[{index}]",
                    f"unknown surface category '{name}'",
                )
            elif name in ("project_state", "authoring_only"):
                report.error(
                    f"bundle-manifest.surface_classes_to_copy[{index}]",
                    f"forbidden bundle surface category '{name}'",
                )

    if ensure_string_list(
        report,
        data.get("primary_entrypoints"),
        "bundle-manifest.primary_entrypoints",
        non_empty=True,
    ):
        for index, path_text in enumerate(data["primary_entrypoints"]):
            validate_repo_path(
                report,
                f"bundle-manifest.primary_entrypoints[{index}]",
                path_text,
                expected_categories=("runtime_public", "runtime_support"),
                forbid_categories=("project_state", "authoring_only"),
            )

    runtime_support = data.get("runtime_support")
    if ensure_dict(report, runtime_support, "bundle-manifest.runtime_support"):
        ensure_required_keys(
            report,
            runtime_support,
            "bundle-manifest.runtime_support",
            ("exact_paths", "globs"),
        )
        if ensure_string_list(
            report,
            runtime_support.get("exact_paths"),
            "bundle-manifest.runtime_support.exact_paths",
        ):
            for index, path_text in enumerate(runtime_support["exact_paths"]):
                validate_repo_path(
                    report,
                    f"bundle-manifest.runtime_support.exact_paths[{index}]",
                    path_text,
                    expected_categories=("runtime_support", "runtime_public"),
                    forbid_categories=("project_state", "authoring_only"),
                )
        if ensure_string_list(
            report,
            runtime_support.get("globs"),
            "bundle-manifest.runtime_support.globs",
        ):
            for index, pattern in enumerate(runtime_support["globs"]):
                report.check()
                matches = sorted(
                    path for path in REPO_ROOT.glob(pattern) if path.is_file()
                )
                if not matches:
                    report.error(
                        f"bundle-manifest.runtime_support.globs[{index}]",
                        f"glob matched no files: {pattern}",
                    )

    ensure_string_list(
        report,
        data.get("exclude_globs"),
        "bundle-manifest.exclude_globs",
    )
    ensure_string_list(
        report,
        data.get("notes"),
        "bundle-manifest.notes",
        non_empty=True,
    )
    return report


def validate_catalog(data: Any, source_path: Path, kind_name: str) -> Report:
    report = Report(kind_name, source_path)
    expectations = CATALOG_EXPECTATIONS[kind_name]

    if not ensure_dict(report, data, kind_name):
        return report
    if not ensure_required_keys(
        report,
        data,
        kind_name,
        ("catalog_version", "catalog_kind", "path_style", "items"),
    ):
        return report

    report.check()
    if not isinstance(data.get("catalog_version"), int):
        report.error(f"{kind_name}.catalog_version", "must be an integer")

    if ensure_string(report, data.get("catalog_kind"), f"{kind_name}.catalog_kind"):
        report.check()
        if data["catalog_kind"] != expectations["catalog_kind"]:
            report.error(
                f"{kind_name}.catalog_kind",
                f"must be '{expectations['catalog_kind']}'",
            )

    if ensure_string(report, data.get("path_style"), f"{kind_name}.path_style"):
        report.check()
        if data["path_style"] != "repository-relative":
            report.error(f"{kind_name}.path_style", "must be 'repository-relative'")

    if kind_name == "sources-catalog":
        validate_repo_path(
            report,
            "sources-catalog.canonical_registry_path",
            data.get("canonical_registry_path"),
            expected_categories=("runtime_support",),
        )
        validate_repo_path(
            report,
            "sources-catalog.citation_audit_path",
            data.get("citation_audit_path"),
            expected_categories=("runtime_support",),
        )

    items = data.get("items")
    if not ensure_list(report, items, f"{kind_name}.items", non_empty=True):
        return report

    seen_ids = set()
    seen_aliases = set()
    for index, item in enumerate(items):
        location = f"{kind_name}.items[{index}]"
        if not ensure_dict(report, item, location):
            continue
        if not ensure_required_keys(
            report, item, location, ("id", "aliases", "path", "status", "kind")
        ):
            continue

        item_id = item.get("id")
        if ensure_string(report, item_id, f"{location}.id"):
            report.check()
            if item_id in seen_ids:
                report.error(f"{location}.id", f"duplicate id '{item_id}'")
            seen_ids.add(item_id)

        aliases = item.get("aliases")
        if ensure_string_list(report, aliases, f"{location}.aliases"):
            for alias_index, alias in enumerate(aliases):
                report.check()
                if alias == item_id:
                    report.error(
                        f"{location}.aliases[{alias_index}]",
                        "must not repeat the canonical id",
                    )
                if alias in seen_aliases:
                    report.error(
                        f"{location}.aliases[{alias_index}]",
                        f"duplicate alias '{alias}'",
                    )
                seen_aliases.add(alias)

        deprecated_aliases = item.get("deprecated_aliases")
        if deprecated_aliases is not None and ensure_string_list(
            report, deprecated_aliases, f"{location}.deprecated_aliases"
        ):
            alias_set = set(item.get("aliases", []))
            for alias_index, alias in enumerate(deprecated_aliases):
                report.check()
                if alias not in alias_set:
                    report.error(
                        f"{location}.deprecated_aliases[{alias_index}]",
                        "must also appear in aliases",
                    )

        if ensure_string(report, item.get("status"), f"{location}.status"):
            report.check()
            if item["status"] not in ALLOWED_STATUSES:
                report.error(
                    f"{location}.status",
                    f"must be one of {', '.join(sorted(ALLOWED_STATUSES))}",
                )

        if ensure_string(report, item.get("kind"), f"{location}.kind"):
            report.check()
            if item["kind"] != expectations["item_kind"]:
                report.error(
                    f"{location}.kind",
                    f"must be '{expectations['item_kind']}'",
                )

        path_text = validate_repo_path(
            report,
            f"{location}.path",
            item.get("path"),
            expected_categories=(expectations["surface_category"],),
            require_exists=item.get("status") != "removed",
            allow_fragment=kind_name == "sources-catalog",
            forbid_categories=("project_state",),
        )
        if path_text is not None:
            normalized_path, fragment = strip_fragment(path_text)
            report.check()
            if not normalized_path.startswith(expectations["path_prefixes"]):
                report.error(
                    f"{location}.path",
                    f"must start with one of {', '.join(expectations['path_prefixes'])}",
                )
            for forbidden_prefix in expectations["generated_prefixes"]:
                report.check()
                if normalized_path.startswith(forbidden_prefix):
                    report.error(
                        f"{location}.path",
                        "must reference hand-authored content, not generated output",
                    )
            if kind_name == "sources-catalog":
                report.check()
                if fragment is None:
                    report.error(
                        f"{location}.path",
                        "must include a source record fragment like '#source-id'",
                    )
                elif item_id is not None and fragment != item_id:
                    report.error(
                        f"{location}.path",
                        f"fragment must match id '{item_id}', found '{fragment}'",
                    )
            elif fragment is not None:
                report.error(f"{location}.path", "must not include a path fragment")

        path_aliases = item.get("path_aliases")
        if path_aliases is not None and ensure_string_list(
            report, path_aliases, f"{location}.path_aliases"
        ):
            for alias_index, alias_path in enumerate(path_aliases):
                validate_repo_path(
                    report,
                    f"{location}.path_aliases[{alias_index}]",
                    alias_path,
                    expected_categories=(expectations["surface_category"],),
                    require_exists=item.get("status") != "removed",
                    forbid_categories=("project_state",),
                )

        if kind_name == "sources-catalog":
            ensure_string(report, item.get("source_type"), f"{location}.source_type")
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

    return report


def validate_global_catalog_integrity(
    catalog_payloads: Dict[str, Dict[str, Any]],
) -> Report:
    report = Report("catalog-integrity", REPO_ROOT / "runtime" / "catalog")
    seen_ids: Dict[str, str] = {}
    seen_aliases: Dict[str, str] = {}

    for kind_name, payload in catalog_payloads.items():
        items = payload.get("items", []) if isinstance(payload, dict) else []
        for item in items:
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if isinstance(item_id, str):
                previous = seen_ids.get(item_id)
                report.check()
                if previous is not None:
                    report.error(
                        "catalog-integrity.ids",
                        f"duplicate id '{item_id}' in {previous} and {kind_name}",
                    )
                else:
                    seen_ids[item_id] = kind_name
            aliases = item.get("aliases", [])
            if isinstance(aliases, list):
                for alias in aliases:
                    if not isinstance(alias, str):
                        continue
                    previous_alias = seen_aliases.get(alias)
                    report.check()
                    if previous_alias is not None:
                        report.error(
                            "catalog-integrity.aliases",
                            f"duplicate alias '{alias}' in {previous_alias} and {kind_name}",
                        )
                    else:
                        seen_aliases[alias] = kind_name
                    report.check()
                    if alias in seen_ids:
                        report.error(
                            "catalog-integrity.aliases",
                            f"alias '{alias}' collides with canonical id from {seen_ids[alias]}",
                        )

    for alias, alias_kind in seen_aliases.items():
        canonical_kind = seen_ids.get(alias)
        report.check()
        if canonical_kind is not None:
            report.error(
                "catalog-integrity.aliases",
                f"alias '{alias}' in {alias_kind} collides with canonical id from {canonical_kind}",
            )

    return report


def infer_kind(path: Path, data: Any) -> Optional[str]:
    name = path.name
    if name == "contract.json":
        return "contract"
    if name == "surface.json":
        return "surface"
    canonical_match = next(
        (kind for kind, candidate in DEFAULT_TARGETS.items() if candidate.name == name),
        None,
    )
    if canonical_match is not None:
        return canonical_match
    if isinstance(data, dict):
        if "consumer_model" in data or "runtime_entrypoints" in data:
            return "contract"
        if any(key in data for key in SURFACE_CATEGORIES):
            return "surface"
        catalog_kind = data.get("catalog_kind")
        if catalog_kind in CATALOG_KIND_TO_NAME:
            return CATALOG_KIND_TO_NAME[catalog_kind]
    return None


def render_report(report: Report) -> None:
    status = "PASS" if report.error_count == 0 else "FAIL"
    print(f"{status} [{report.label}] {report.source_path}")
    for issue in report.issues:
        print(f"  {issue.severity} {issue.location}: {issue.message}")
    if report.warning_count and report.error_count == 0:
        print(f"  warnings: {report.warning_count}")
    print(f"  checks: {report.checks}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate runtime contract JSON artifacts."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate contract, surface, and all runtime catalogs.",
    )
    parser.add_argument("--file", help="Validate a single JSON file.")
    parser.add_argument(
        "--kind",
        choices=sorted(DEFAULT_TARGETS.keys()),
        help="Validate a canonical target kind or force the kind for --file.",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit non-zero when warnings are present.",
    )
    args = parser.parse_args()
    if args.all and (args.file or args.kind):
        parser.error("--all cannot be combined with --file or --kind")
    if not args.all and not args.file and not args.kind:
        parser.error("choose one of --all, --file, or --kind")
    return args


def resolve_input_file(file_arg: str) -> Path:
    return Path(file_arg).expanduser().resolve()


def validate_target(
    kind_name: str, source_path: Path
) -> Tuple[Report, Optional[Dict[str, Any]]]:
    data, error = load_json(source_path)
    if error is not None:
        report = Report(kind_name, source_path)
        report.error(kind_name, error)
        return report, None
    if kind_name == "contract":
        return validate_contract(data, source_path), data if isinstance(
            data, dict
        ) else None
    if kind_name == "surface":
        return validate_surface(data, source_path), data if isinstance(
            data, dict
        ) else None
    if kind_name == "auto-intake-contract":
        return validate_auto_intake_contract(data, source_path), data if isinstance(
            data, dict
        ) else None
    if kind_name == "bundle-manifest":
        return validate_bundle_manifest(data, source_path), data if isinstance(
            data, dict
        ) else None
    return validate_catalog(data, source_path, kind_name), data if isinstance(
        data, dict
    ) else None


def main() -> int:
    args = parse_args()
    reports: List[Report] = []
    loaded_catalogs: Dict[str, Dict[str, Any]] = {}

    if args.all:
        for kind_name in (
            "contract",
            "surface",
            "auto-intake-contract",
            "bundle-manifest",
            "scenarios-catalog",
            "playbooks-catalog",
            "nodes-catalog",
            "prompts-catalog",
            "sources-catalog",
        ):
            report, payload = validate_target(kind_name, DEFAULT_TARGETS[kind_name])
            reports.append(report)
            if payload is not None and kind_name.endswith("-catalog"):
                loaded_catalogs[kind_name] = payload
        reports.append(validate_global_catalog_integrity(loaded_catalogs))
    else:
        source_path = (
            resolve_input_file(args.file) if args.file else DEFAULT_TARGETS[args.kind]
        )
        data, error = load_json(source_path)
        if error is not None:
            report = Report(args.kind or "unknown", source_path)
            report.error(args.kind or "unknown", error)
            reports.append(report)
        else:
            kind_name = args.kind or infer_kind(source_path, data)
            if kind_name is None:
                report = Report("unknown", source_path)
                report.error("kind", "could not infer file kind; use --kind")
                reports.append(report)
            elif kind_name == "contract":
                reports.append(validate_contract(data, source_path))
            elif kind_name == "surface":
                reports.append(validate_surface(data, source_path))
            elif kind_name == "auto-intake-contract":
                reports.append(validate_auto_intake_contract(data, source_path))
            elif kind_name == "bundle-manifest":
                reports.append(validate_bundle_manifest(data, source_path))
            else:
                reports.append(validate_catalog(data, source_path, kind_name))

    for report in reports:
        render_report(report)

    total_checks = sum(report.checks for report in reports)
    total_errors = sum(report.error_count for report in reports)
    total_warnings = sum(report.warning_count for report in reports)
    failed_targets = sum(1 for report in reports if report.error_count > 0)
    validated_targets = len(reports)
    print(
        f"Summary: validated {validated_targets} target(s), {total_checks} checks, "
        f"{total_errors} error(s), {total_warnings} warning(s), {failed_targets} failed target(s)."
    )

    if total_errors:
        return 1
    if args.fail_on_warning and total_warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
