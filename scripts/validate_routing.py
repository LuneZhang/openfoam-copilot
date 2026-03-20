#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from typing import List

from routing_runtime import (
    discover_fixture_files,
    load_fixture_cases,
    load_fixture_schema,
    load_routing_inputs,
    render_report,
    validate_fixture_collection,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate routing fixtures and routing doc references."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all routing fixtures plus current routing docs.",
    )
    parser.add_argument(
        "--fixture",
        help="Validate a single routing fixture suite JSON file.",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit non-zero when warnings are present.",
    )
    args = parser.parse_args()
    if args.all and args.fixture:
        parser.error("--all cannot be combined with --fixture")
    if not args.all and not args.fixture:
        parser.error("choose --all or --fixture")
    return args


def main() -> int:
    args = parse_args()
    reports: List = []

    schema_report, schema = load_fixture_schema()
    reports.append(schema_report)

    (
        routing_reports,
        scenario_registry,
        playbook_registry,
        node_registry,
        _scenario_map,
        _playbook_map,
    ) = load_routing_inputs()
    reports.extend(routing_reports)

    if (
        schema is None
        or scenario_registry is None
        or playbook_registry is None
        or node_registry is None
    ):
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
        return 1

    if args.all:
        fixture_paths = discover_fixture_files()
    else:
        fixture_paths = [Path(args.fixture).expanduser().resolve()]

    if not fixture_paths:
        missing_report = validate_fixture_collection([])
        reports.append(missing_report)
    else:
        fixture_reports, _cases = load_fixture_cases(
            fixture_paths, schema, scenario_registry, playbook_registry, node_registry
        )
        reports.extend(fixture_reports)

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
