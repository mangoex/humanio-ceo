#!/usr/bin/env python3
"""Verify that officially validated plugin artifacts have not changed."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = (
    ROOT / "pilots/humanio-ceo/evidence/official-validation.json"
)
CONTRACT_PATH = ".codex-plugin/validation-contract.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_contract(root: Path = ROOT) -> dict[str, Any]:
    payload = json.loads((root / CONTRACT_PATH).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("validation contract must be a JSON object")
    required_skills = payload.get("required_skills")
    dependencies = payload.get("skill_dependencies")
    if (
        not isinstance(required_skills, list)
        or not required_skills
        or not all(isinstance(name, str) and name for name in required_skills)
        or len(required_skills) != len(set(required_skills))
    ):
        raise ValueError("required_skills must be a unique non-empty string list")
    if (
        not isinstance(dependencies, list)
        or not all(isinstance(path, str) and path for path in dependencies)
        or len(dependencies) != len(set(dependencies))
    ):
        raise ValueError("skill_dependencies must be a unique string list")
    return payload


def installed_skills(root: Path = ROOT) -> set[str]:
    skills_root = root / "skills"
    return {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }


def expected_artifacts(root: Path, contract: dict[str, Any]) -> set[str]:
    artifacts = {
        ".codex-plugin/plugin.json",
        CONTRACT_PATH,
        *contract["skill_dependencies"],
    }
    for name in contract["required_skills"]:
        skill_root = root / "skills" / name
        if not skill_root.is_dir():
            continue
        for path in skill_root.rglob("*"):
            relative_parts = path.relative_to(skill_root).parts
            if (
                path.is_file()
                and not any(part.startswith(".") for part in relative_parts)
                and "__pycache__" not in relative_parts
                and path.suffix != ".pyc"
            ):
                artifacts.add(path.relative_to(root).as_posix())
    return artifacts


def verify(payload: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        contract = load_contract(root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"invalid validation contract: {error}"]
    required_skills = set(contract["required_skills"])
    if payload.get("plugin_result") != "passed":
        errors.append("official plugin validation is not recorded as passed")
    discovered_skills = installed_skills(root)
    if discovered_skills != required_skills:
        errors.append(
            "installed skills must match the canonical inventory exactly: "
            f"expected {sorted(required_skills)}, "
            f"got {sorted(discovered_skills)}"
        )
    skill_results = payload.get("skill_results")
    if not isinstance(skill_results, dict):
        errors.append("skill_results must be an object")
    elif set(skill_results) != required_skills:
        errors.append(
            "skill_results must match canonical skills exactly: "
            f"expected {sorted(required_skills)}, got {sorted(skill_results)}"
        )
    elif set(skill_results.values()) != {"passed"}:
        errors.append("all official skill validations must be passed")
    artifacts = payload.get("artifact_sha256")
    if not isinstance(artifacts, dict) or not artifacts:
        errors.append("artifact_sha256 must be a non-empty object")
        return errors
    required_artifacts = expected_artifacts(root, contract)
    if set(artifacts) != required_artifacts:
        errors.append(
            "artifact_sha256 must match the validation contract and all skill inputs "
            f"exactly: expected {sorted(required_artifacts)}, "
            f"got {sorted(artifacts)}"
        )
    for relative, expected in sorted(artifacts.items()):
        path = root / relative
        if not path.is_file():
            errors.append(f"validated artifact is missing: {relative}")
            continue
        actual = digest(path)
        if actual != expected:
            errors.append(f"validated artifact changed: {relative}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify official validation evidence.")
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.evidence.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        print("ERROR: official evidence must be a JSON object.", file=sys.stderr)
        return 2
    errors = verify(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Evidencia oficial vigente: {len(payload['artifact_sha256'])} artefactos."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
