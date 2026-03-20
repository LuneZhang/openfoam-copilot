#!/usr/bin/env python3

import argparse
import json
import shutil
import sys
import tempfile
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from validate_contract import REPO_ROOT, classify_surface, normalize_path


RUNTIME_ROOT = REPO_ROOT / "runtime"
BUNDLE_MANIFEST_PATH = RUNTIME_ROOT / "bundle-manifest.json"
SURFACE_PATH = RUNTIME_ROOT / "surface.json"
SURFACE_CLASSES = (
    "runtime_public",
    "runtime_support",
    "authoring_only",
    "project_state",
)
FORBIDDEN_CLASSES = {"project_state", "authoring_only"}


class BundleExportError(Exception):
    pass


def repo_relative(path: Path) -> str:
    return normalize_path(str(path.relative_to(REPO_ROOT)))


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BundleExportError(f"missing JSON file: {repo_relative(path)}") from exc
    except json.JSONDecodeError as exc:
        raise BundleExportError(
            f"invalid JSON in {repo_relative(path)} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def require_object(value: Any, label: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise BundleExportError(f"{label} must be a JSON object")
    return value


def require_list(value: Any, label: str) -> List[Any]:
    if not isinstance(value, list):
        raise BundleExportError(f"{label} must be a JSON array")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BundleExportError(f"{label} must be a non-empty string")
    return value.strip()


def require_string_list(
    value: Any, label: str, *, non_empty: bool = False
) -> List[str]:
    items = require_list(value, label)
    result: List[str] = []
    for index, item in enumerate(items):
        result.append(require_string(item, f"{label}[{index}]"))
    if non_empty and not result:
        raise BundleExportError(f"{label} must not be empty")
    return result


def load_surface() -> Dict[str, Any]:
    surface = require_object(load_json(SURFACE_PATH), "surface")
    for category in SURFACE_CLASSES:
        require_string_list(
            surface.get(category), f"surface.{category}", non_empty=True
        )
    return surface


def load_bundle_manifest() -> Dict[str, Any]:
    manifest = require_object(load_json(BUNDLE_MANIFEST_PATH), "bundle_manifest")
    require_string(manifest.get("bundle_name"), "bundle_manifest.bundle_name")
    require_string(manifest.get("consumer_model"), "bundle_manifest.consumer_model")
    require_string(manifest.get("output_manifest"), "bundle_manifest.output_manifest")
    require_string_list(
        manifest.get("primary_entrypoints"),
        "bundle_manifest.primary_entrypoints",
        non_empty=True,
    )
    require_string_list(
        manifest.get("surface_classes_to_copy"),
        "bundle_manifest.surface_classes_to_copy",
        non_empty=True,
    )
    runtime_support = require_object(
        manifest.get("runtime_support"), "bundle_manifest.runtime_support"
    )
    require_string_list(
        runtime_support.get("exact_paths"),
        "bundle_manifest.runtime_support.exact_paths",
    )
    require_string_list(
        runtime_support.get("globs"), "bundle_manifest.runtime_support.globs"
    )
    require_string_list(manifest.get("exclude_globs"), "bundle_manifest.exclude_globs")
    require_string_list(manifest.get("notes"), "bundle_manifest.notes")
    return manifest


def ensure_known_surface_class(name: str) -> str:
    if name not in SURFACE_CLASSES:
        raise BundleExportError(
            f"unknown surface class '{name}' in runtime/bundle-manifest.json"
        )
    return name


def classify_path(path_text: str, surface: Dict[str, Any]) -> str:
    category, matches = classify_surface(path_text, surface)
    if category is None:
        if matches:
            raise BundleExportError(
                f"path matches multiple surface classes for bundle export: {path_text} -> {', '.join(matches)}"
            )
        raise BundleExportError(
            f"path is not classified by runtime/surface.json for bundle export: {path_text}"
        )
    return category


def matches_any(path_text: str, patterns: Sequence[str]) -> bool:
    return any(fnmatch(path_text, pattern) for pattern in patterns)


def iter_repo_files() -> List[str]:
    return sorted(
        repo_relative(path) for path in REPO_ROOT.rglob("*") if path.is_file()
    )


def resolve_exact_path(
    path_text: str,
    *,
    surface: Dict[str, Any],
    exclude_globs: Sequence[str],
) -> Optional[Tuple[str, str]]:
    normalized = normalize_path(path_text)
    source_path = REPO_ROOT / normalized
    if not source_path.exists() or not source_path.is_file():
        raise BundleExportError(
            f"bundle input path does not exist as a file: {normalized}"
        )
    if matches_any(normalized, exclude_globs):
        return None
    category = classify_path(normalized, surface)
    if category in FORBIDDEN_CLASSES:
        raise BundleExportError(
            f"bundle input path is forbidden by runtime surface classification: {normalized} -> {category}"
        )
    return normalized, category


def expand_glob_pattern(
    pattern: str,
    *,
    surface: Dict[str, Any],
    exclude_globs: Sequence[str],
) -> Set[Tuple[str, str]]:
    matches: Set[Tuple[str, str]] = set()
    for path in REPO_ROOT.glob(pattern):
        if not path.is_file():
            continue
        relative = repo_relative(path)
        if matches_any(relative, exclude_globs):
            continue
        category = classify_path(relative, surface)
        if category in FORBIDDEN_CLASSES:
            raise BundleExportError(
                f"bundle glob matched forbidden file by runtime surface classification: {relative} -> {category}"
            )
        matches.add((relative, category))
    if not matches:
        raise BundleExportError(f"bundle glob matched no files: {pattern}")
    return matches


def collect_runtime_public_files(
    *,
    surface: Dict[str, Any],
    classes_to_copy: Sequence[str],
    exclude_globs: Sequence[str],
) -> Dict[str, Set[str]]:
    selected: Dict[str, Set[str]] = {name: set() for name in SURFACE_CLASSES}
    target_classes = {ensure_known_surface_class(name) for name in classes_to_copy}
    for path_text in iter_repo_files():
        if matches_any(path_text, exclude_globs):
            continue
        category, matches = classify_surface(path_text, surface)
        if category is None:
            if matches:
                raise BundleExportError(
                    f"path matches multiple surface classes for bundle export: {path_text} -> {', '.join(matches)}"
                )
            continue
        if category in target_classes:
            if category in FORBIDDEN_CLASSES:
                raise BundleExportError(
                    f"refusing to copy forbidden surface class '{category}' from {path_text}"
                )
            selected[category].add(path_text)
    return selected


def collect_runtime_support_files(
    *,
    surface: Dict[str, Any],
    manifest: Dict[str, Any],
    exclude_globs: Sequence[str],
) -> Dict[str, Set[str]]:
    selected: Dict[str, Set[str]] = {name: set() for name in SURFACE_CLASSES}
    runtime_support = require_object(
        manifest.get("runtime_support"), "bundle_manifest.runtime_support"
    )
    exact_paths = require_string_list(
        runtime_support.get("exact_paths"),
        "bundle_manifest.runtime_support.exact_paths",
    )
    glob_patterns = require_string_list(
        runtime_support.get("globs"), "bundle_manifest.runtime_support.globs"
    )

    for path_text in exact_paths:
        resolved = resolve_exact_path(
            path_text, surface=surface, exclude_globs=exclude_globs
        )
        if resolved is None:
            continue
        normalized, category = resolved
        selected[category].add(normalized)

    for pattern in glob_patterns:
        for normalized, category in expand_glob_pattern(
            pattern, surface=surface, exclude_globs=exclude_globs
        ):
            selected[category].add(normalized)
    return selected


def ensure_primary_entrypoints(
    files: Set[str],
    *,
    surface: Dict[str, Any],
    manifest: Dict[str, Any],
    exclude_globs: Sequence[str],
) -> List[str]:
    primary_entrypoints = require_string_list(
        manifest.get("primary_entrypoints"),
        "bundle_manifest.primary_entrypoints",
        non_empty=True,
    )
    resolved_entrypoints: List[str] = []
    for path_text in primary_entrypoints:
        resolved = resolve_exact_path(
            path_text, surface=surface, exclude_globs=exclude_globs
        )
        if resolved is None:
            raise BundleExportError(
                f"primary entrypoint is excluded by bundle rules: {path_text}"
            )
        normalized, category = resolved
        if category in FORBIDDEN_CLASSES:
            raise BundleExportError(
                f"primary entrypoint cannot come from forbidden class '{category}': {normalized}"
            )
        if normalized not in files:
            raise BundleExportError(
                f"primary entrypoint is not included in exported files: {normalized}"
            )
        resolved_entrypoints.append(normalized)
    return resolved_entrypoints


def copy_files(files: Iterable[str], destination_root: Path) -> None:
    for path_text in sorted(files):
        source_path = REPO_ROOT / path_text
        destination_path = destination_root / path_text
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)


def write_output_manifest(
    destination_root: Path,
    *,
    manifest: Dict[str, Any],
    primary_entrypoints: Sequence[str],
    files_by_class: Dict[str, Set[str]],
) -> None:
    output_manifest_name = require_string(
        manifest.get("output_manifest"), "bundle_manifest.output_manifest"
    )
    ordered_files = sorted(
        file_path for paths in files_by_class.values() for file_path in paths
    )
    payload = {
        "manifest_version": manifest.get("manifest_version"),
        "bundle_name": manifest.get("bundle_name"),
        "consumer_model": manifest.get("consumer_model"),
        "source_manifest": repo_relative(BUNDLE_MANIFEST_PATH),
        "output_manifest": output_manifest_name,
        "primary_entrypoints": list(primary_entrypoints),
        "included_surface_classes": [
            name
            for name in ("runtime_public", "runtime_support")
            if files_by_class[name]
        ],
        "excluded_surface_classes": sorted(FORBIDDEN_CLASSES),
        "counts": {
            "files": len(ordered_files),
            "runtime_public": len(files_by_class["runtime_public"]),
            "runtime_support": len(files_by_class["runtime_support"]),
        },
        "files": ordered_files,
        "files_by_class": {
            "runtime_public": sorted(files_by_class["runtime_public"]),
            "runtime_support": sorted(files_by_class["runtime_support"]),
        },
        "notes": require_string_list(manifest.get("notes"), "bundle_manifest.notes"),
    }
    output_path = destination_root / output_manifest_name
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the minimal runtime bundle for external coding agents."
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for the exported runtime bundle.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.out).expanduser()
    if not output_dir.is_absolute():
        output_dir = (Path.cwd() / output_dir).resolve()

    surface = load_surface()
    manifest = load_bundle_manifest()
    exclude_globs = require_string_list(
        manifest.get("exclude_globs"), "bundle_manifest.exclude_globs"
    )
    classes_to_copy = require_string_list(
        manifest.get("surface_classes_to_copy"),
        "bundle_manifest.surface_classes_to_copy",
        non_empty=True,
    )

    files_by_class = {name: set() for name in SURFACE_CLASSES}
    runtime_public_files = collect_runtime_public_files(
        surface=surface,
        classes_to_copy=classes_to_copy,
        exclude_globs=exclude_globs,
    )
    runtime_support_files = collect_runtime_support_files(
        surface=surface,
        manifest=manifest,
        exclude_globs=exclude_globs,
    )

    for category in SURFACE_CLASSES:
        files_by_class[category].update(runtime_public_files.get(category, set()))
        files_by_class[category].update(runtime_support_files.get(category, set()))

    if files_by_class["project_state"]:
        leaked = ", ".join(sorted(files_by_class["project_state"]))
        raise BundleExportError(
            f"project_state files leaked into bundle selection: {leaked}"
        )
    if files_by_class["authoring_only"]:
        leaked = ", ".join(sorted(files_by_class["authoring_only"]))
        raise BundleExportError(
            f"authoring_only files leaked into bundle selection: {leaked}"
        )

    all_files = set().union(
        files_by_class["runtime_public"], files_by_class["runtime_support"]
    )
    primary_entrypoints = ensure_primary_entrypoints(
        all_files,
        surface=surface,
        manifest=manifest,
        exclude_globs=exclude_globs,
    )

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_root = Path(
        tempfile.mkdtemp(prefix="openfoam-copilot-runtime-", dir=str(output_dir.parent))
    )
    try:
        copy_files(all_files, temp_root)
        write_output_manifest(
            temp_root,
            manifest=manifest,
            primary_entrypoints=primary_entrypoints,
            files_by_class=files_by_class,
        )
        if output_dir.exists():
            if output_dir.is_dir():
                shutil.rmtree(output_dir)
            else:
                output_dir.unlink()
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(temp_root), str(output_dir))
    except Exception:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise

    print(f"Exported runtime bundle to {output_dir}")
    print(f"- runtime_public files: {len(files_by_class['runtime_public'])}")
    print(f"- runtime_support files: {len(files_by_class['runtime_support'])}")
    print(f"- total copied files: {len(all_files)}")
    print(
        f"- output manifest: {output_dir / require_string(manifest.get('output_manifest'), 'bundle_manifest.output_manifest')}"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BundleExportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
