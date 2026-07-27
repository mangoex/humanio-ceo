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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def installed_skills() -> set[str]:
    skills_root = ROOT / "skills"
    return {path.name for path in skills_root.iterdir() if path.is_dir()}


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("plugin_result") != "passed":
        errors.append("official plugin validation is not recorded as passed")
    expected_skills = installed_skills()
    skill_results = payload.get("skill_results")
    if not isinstance(skill_results, dict):
        errors.append("skill_results must be an object")
    elif set(skill_results) != expected_skills:
        errors.append(
            "skill_results must match installed skills exactly: "
            f"expected {sorted(expected_skills)}, got {sorted(skill_results)}"
        )
    elif set(skill_results.values()) != {"passed"}:
        errors.append("all official skill validations must be passed")
    artifacts = payload.get("artifact_sha256")
    if not isinstance(artifacts, dict) or not artifacts:
        errors.append("artifact_sha256 must be a non-empty object")
        return errors
    expected_artifacts = {".codex-plugin/plugin.json"} | {
        f"skills/{name}/SKILL.md" for name in expected_skills
    }
    if set(artifacts) != expected_artifacts:
        errors.append(
            "artifact_sha256 must match the plugin manifest and installed skills "
            f"exactly: expected {sorted(expected_artifacts)}, "
            f"got {sorted(artifacts)}"
        )
    for relative, expected in sorted(artifacts.items()):
        path = ROOT / relative
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
