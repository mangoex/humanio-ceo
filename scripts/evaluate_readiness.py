#!/usr/bin/env python3
"""Execute deterministic readiness decision cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CASE_NAMES = {
    "strict validation failed",
    "tests not executed",
    "approval missing",
    "accepted residual condition",
    "all gates passed",
}


def decide(case: dict[str, Any]) -> str:
    if case.get("strict_exit_code") != 0:
        return "NOT READY"
    if case.get("tests_passed") is not True:
        return "NOT READY"
    if case.get("required_approvals") is not True:
        return "NOT READY"
    if case.get("accepted_conditions"):
        return "CONDITIONAL"
    return "READY"


def evaluate(cases: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, case in enumerate(cases, start=1):
        actual = decide(case)
        expected = case.get("expected")
        if actual != expected:
            errors.append(
                f"case {index} ({case.get('name', 'unnamed')}): "
                f"expected {expected}, got {actual}"
            )
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate readiness policy cases.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=ROOT / "tests/evals/readiness-cases.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if not isinstance(payload, list) or not all(
        isinstance(item, dict) for item in payload
    ):
        print("ERROR: el archivo de casos debe contener una lista de objetos.", file=sys.stderr)
        return 2
    case_names = [item.get("name") for item in payload]
    if (
        len(payload) != len(REQUIRED_CASE_NAMES)
        or any(not isinstance(name, str) for name in case_names)
        or set(case_names) != REQUIRED_CASE_NAMES
    ):
        print(
            "ERROR: se requiere el conjunto completo y sin duplicados de "
            f"{len(REQUIRED_CASE_NAMES)} casos de readiness.",
            file=sys.stderr,
        )
        return 2
    errors = evaluate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PBD-T-001 aprobado: {len(payload)} casos de readiness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
