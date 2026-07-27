#!/usr/bin/env python3
"""Execute deterministic readiness decision cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".codex-plugin/validation-contract.json"
CASE_TYPES = {
    "name": str,
    "strict_exit_code": int,
    "tests_passed": bool,
    "required_approvals": bool,
    "accepted_conditions": bool,
    "expected": str,
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


def load_required_cases() -> dict[str, dict[str, Any]]:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    cases = contract.get("required_readiness_cases")
    if not isinstance(cases, list) or not all(
        isinstance(case, dict) for case in cases
    ):
        raise ValueError(
            "required_readiness_cases must be a list of objects"
        )
    names = [case.get("name") for case in cases]
    if (
        not cases
        or any(not isinstance(name, str) for name in names)
        or len(names) != len(set(names))
    ):
        raise ValueError(
            "canonical readiness case names must be unique strings"
        )
    return {case["name"]: case for case in cases}


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
        required_cases = load_required_cases()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if not isinstance(payload, list) or not all(
        isinstance(item, dict) for item in payload
    ):
        print("ERROR: el archivo de casos debe contener una lista de objetos.", file=sys.stderr)
        return 2
    case_names = [item.get("name") for item in payload]
    if (
        len(payload) != len(required_cases)
        or any(not isinstance(name, str) for name in case_names)
        or set(case_names) != set(required_cases)
    ):
        print(
            "ERROR: se requiere el conjunto completo y sin duplicados de "
            f"{len(required_cases)} casos de readiness.",
            file=sys.stderr,
        )
        return 2
    for case in payload:
        name = case["name"]
        expected_case = required_cases[name]
        if set(case) != set(CASE_TYPES) or any(
            type(case[field]) is not expected_type
            for field, expected_type in CASE_TYPES.items()
        ):
            print(
                f"ERROR: el caso {name!r} contiene campos o tipos no canónicos.",
                file=sys.stderr,
            )
            return 2
        if case != expected_case:
            print(
                f"ERROR: el caso {name!r} no coincide con su escenario canónico.",
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
