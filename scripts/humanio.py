#!/usr/bin/env python3
"""Unified command-line entry point for Humanio CEO."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".codex-plugin/validation-contract.json"


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(prog="humanio", description="Humanio CEO toolkit.")
    commands = cli.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Initialize a governed project.")
    init.add_argument("--project", required=True)
    init.add_argument(
        "--profile", required=True, choices=("conversational", "software", "hybrid")
    )
    init.add_argument("--risk", required=True, choices=("R0", "R1", "R2", "R3"))
    init.add_argument("--output", required=True, type=Path)

    validate = commands.add_parser("validate", help="Validate a project workspace.")
    validate.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
    validate.add_argument("--strict", action="store_true")
    validate.add_argument("--json", action="store_true")

    commands.add_parser("doctor", help="Check the plugin installation.")
    return cli


def run_script(name: str, arguments: list[str]) -> int:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), *arguments],
        check=False,
    )
    return result.returncode


def doctor() -> int:
    try:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        required_skills = contract["required_skills"]
        if (
            not isinstance(required_skills, list)
            or not required_skills
            or not all(isinstance(name, str) and name for name in required_skills)
        ):
            raise ValueError("required_skills inválido")
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(
            f"Humanio CEO doctor: contrato de validación inválido: {error}",
            file=sys.stderr,
        )
        return 1
    required = (
        ".codex-plugin/plugin.json",
        ".codex-plugin/validation-contract.json",
        "docs/framework/00-CONSTITUTION.md",
        "scripts/init_project.py",
        "scripts/validate_workspace.py",
        "schemas/humanio.schema.json",
        *(f"skills/{name}/SKILL.md" for name in required_skills),
        "templates/common/PROJECT_MANIFEST.yaml",
        "templates/conversational/01-CONSTITUTION.md",
        "templates/software/02-PRD.md",
        "VERSION",
    )
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        print("Humanio CEO doctor: instalación incompleta.", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    plugin = json.loads(
        (ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    manifest = (ROOT / "templates/common/PROJECT_MANIFEST.yaml").read_text(
        encoding="utf-8"
    )
    if plugin.get("version") != version or f'framework_version: "{version}"' not in manifest:
        print(
            "Humanio CEO doctor: VERSION, plugin.json y plantilla no coinciden.",
            file=sys.stderr,
        )
        return 1
    print("Humanio CEO doctor: instalación válida.")
    return 0


def main() -> int:
    args = parser().parse_args()
    if args.command == "doctor":
        return doctor()
    if args.command == "init":
        return run_script(
            "init_project.py",
            [
                "--project",
                args.project,
                "--profile",
                args.profile,
                "--risk",
                args.risk,
                "--output",
                str(args.output),
            ],
        )
    arguments = [str(args.workspace)]
    if args.strict:
        arguments.append("--strict")
    if args.json:
        arguments.append("--json")
    return run_script("validate_workspace.py", arguments)


if __name__ == "__main__":
    raise SystemExit(main())
