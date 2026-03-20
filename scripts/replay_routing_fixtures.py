#!/usr/bin/env python3

import argparse
import sys

from routing_runtime import (
    discover_fixture_files,
    evaluate_case_expectations,
    load_fixture_cases,
    load_fixture_schema,
    load_routing_inputs,
    ranked_nodes_for_case,
    render_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replay routing fixtures against current routing docs."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Replay every routing fixture case.",
    )
    parser.add_argument(
        "--suite",
        help="Replay only fixture cases whose suite matches this value.",
    )
    args = parser.parse_args()
    if args.all and args.suite:
        parser.error("--all cannot be combined with --suite")
    if not args.all and not args.suite:
        parser.error("choose --all or --suite")
    return args


def main() -> int:
    args = parse_args()

    schema_report, schema = load_fixture_schema()
    (
        routing_reports,
        scenario_registry,
        playbook_registry,
        node_registry,
        scenario_map,
        playbook_map,
    ) = load_routing_inputs()
    preflight_reports = [schema_report] + routing_reports
    preflight_errors = sum(report.error_count for report in preflight_reports)

    if (
        preflight_errors
        or schema is None
        or scenario_registry is None
        or playbook_registry is None
        or node_registry is None
    ):
        for report in preflight_reports:
            render_report(report)
        total_checks = sum(report.checks for report in preflight_reports)
        total_errors = sum(report.error_count for report in preflight_reports)
        total_warnings = sum(report.warning_count for report in preflight_reports)
        failed_targets = sum(
            1 for report in preflight_reports if report.error_count > 0
        )
        print(
            f"Summary: validated {len(preflight_reports)} preflight target(s), {total_checks} checks, "
            f"{total_errors} error(s), {total_warnings} warning(s), {failed_targets} failed target(s)."
        )
        return 1

    fixture_paths = discover_fixture_files()
    fixture_reports, cases = load_fixture_cases(
        fixture_paths, schema, scenario_registry, playbook_registry, node_registry
    )
    for report in preflight_reports + fixture_reports:
        if report.error_count:
            render_report(report)
    if sum(report.error_count for report in fixture_reports):
        total_reports = preflight_reports + fixture_reports
        total_checks = sum(report.checks for report in total_reports)
        total_errors = sum(report.error_count for report in total_reports)
        total_warnings = sum(report.warning_count for report in total_reports)
        failed_targets = sum(1 for report in total_reports if report.error_count > 0)
        print(
            f"Summary: validated {len(total_reports)} target(s), {total_checks} checks, "
            f"{total_errors} error(s), {total_warnings} warning(s), {failed_targets} failed target(s)."
        )
        return 1

    if args.suite:
        cases = [case for case in cases if case.suite == args.suite]
    if not cases:
        selector = args.suite if args.suite else "all"
        print(f"FAIL [routing-replay] no fixture cases matched selector '{selector}'")
        print("Summary: replayed 0 case(s), 1 failed case(s).")
        return 1

    passed = 0
    failed = 0
    for case in cases:
        ranked_nodes = ranked_nodes_for_case(case, scenario_map, playbook_map)
        ok, reasons = evaluate_case_expectations(case, ranked_nodes)
        top_preview = ", ".join(ranked_nodes[:5])
        status = "PASS" if ok else "FAIL"
        print(
            f"{status} [{case.case_id}] suite={case.suite} matrix={case.matrix_ref} "
            f"scenario={case.scenario_id} playbook={case.playbook_id} top={top_preview}"
        )
        if ok:
            passed += 1
            continue
        failed += 1
        for reason in reasons:
            print(f"  ERROR {reason}")

    print(f"Summary: replayed {len(cases)} case(s), {passed} passed, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
