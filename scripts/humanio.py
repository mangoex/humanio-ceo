#!/usr/bin/env python3
"""Unified command-line entry point for Humanio CEO."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import adapters


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
    init.add_argument(
        "--adopt",
        action="store_true",
        help="Preserve existing README.md and AGENTS.md while adopting a repository.",
    )

    validate = commands.add_parser("validate", help="Validate a project workspace.")
    validate.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
    validate.add_argument("--strict", action="store_true")
    validate.add_argument("--json", action="store_true")

    commands.add_parser("doctor", help="Check the framework installation.")

    detect = commands.add_parser(
        "detect", help="Detect explicit IDE and agent signals in a project."
    )
    detect.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
    detect.add_argument("--json", action="store_true")

    for name, help_text in (
        ("install", "Install one or more project adapters."),
        ("integrate", "Alias for project adapter installation."),
    ):
        integrate = commands.add_parser(name, help=help_text)
        integrate.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
        integrate.add_argument(
            "--adapter",
            action="append",
            choices=("auto", "all", *adapters.ADAPTERS),
            default=[],
        )
        integrate.add_argument("--dry-run", action="store_true")

    sync = commands.add_parser("sync", help="Regenerate installed adapter blocks.")
    sync.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
    sync.add_argument("--dry-run", action="store_true")

    uninstall = commands.add_parser(
        "uninstall", help="Remove project adapters without deleting user content."
    )
    uninstall.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
    uninstall.add_argument(
        "--adapter",
        action="append",
        choices=("all", *adapters.ADAPTERS),
        default=[],
    )
    uninstall.add_argument("--dry-run", action="store_true")

    status = commands.add_parser("status", help="Inspect installed adapters and drift.")
    status.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
    status.add_argument("--json", action="store_true")
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
        "scripts/install_cli.py",
        "scripts/adapters.py",
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


def print_changes(
    installed: list[str], changes: list[adapters.Change], dry_run: bool
) -> None:
    print(f"Adaptadores activos: {', '.join(installed) if installed else 'ninguno'}")
    prefix = "DRY-RUN" if dry_run else "OK"
    if not changes:
        print(f"{prefix}: sin cambios")
    for change in changes:
        print(f"{prefix}: {change.action} {change.path.as_posix()}")


def adapter_command(args: argparse.Namespace) -> int:
    try:
        if args.command in ("install", "integrate"):
            active, changes = adapters.install(
                args.workspace, args.adapter, args.dry_run
            )
        elif args.command == "sync":
            active, changes = adapters.sync(args.workspace, args.dry_run)
        else:
            active, changes = adapters.uninstall(
                args.workspace, args.adapter, args.dry_run
            )
    except (OSError, adapters.AdapterError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print_changes(active, changes, args.dry_run)
    return 0


def main() -> int:
    args = parser().parse_args()
    if args.command == "doctor":
        return doctor()
    if args.command == "detect":
        try:
            found = adapters.detect(args.workspace)
        except adapters.AdapterError as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
        if args.json:
            print(
                json.dumps(
                    {"workspace": str(args.workspace.resolve()), "adapters": found}
                )
            )
        else:
            print(f"Adaptadores detectados: {', '.join(found)}")
        return 0
    if args.command in ("install", "integrate", "sync", "uninstall"):
        return adapter_command(args)
    if args.command == "status":
        try:
            report = adapters.status(args.workspace)
        except (OSError, adapters.AdapterError) as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(
                f"Humanio adapters: {'válidos' if report['healthy'] else 'con deriva'}"
            )
            print(
                "Activos: "
                + (", ".join(report["adapters"]) if report["adapters"] else "ninguno")
            )
            for path, state in report["targets"].items():
                print(f"  - {path}: {state}")
        return 0 if report["healthy"] else 1
    if args.command == "init":
        arguments = [
            "--project",
            args.project,
            "--profile",
            args.profile,
            "--risk",
            args.risk,
            "--output",
            str(args.output),
        ]
        if args.adopt:
            arguments.append("--adopt")
        return run_script("init_project.py", arguments)
    arguments = [str(args.workspace)]
    if args.strict:
        arguments.append("--strict")
    if args.json:
        arguments.append("--json")
    return run_script("validate_workspace.py", arguments)


if __name__ == "__main__":
    raise SystemExit(main())
