#!/usr/bin/env python3
"""Initialize a Humanio CEO project without overwriting existing files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROFILES = ("conversational", "software", "hybrid")
RISKS = ("R0", "R1", "R2", "R3")

COMMON_FILES = {
    "common/PROJECT_MANIFEST.yaml": "humanio.yaml",
    "common/08-RISK-REGISTER.md": "docs/08-registro-riesgos.md",
    "common/09-CHANGE-LOG.md": "docs/09-registro-cambios.md",
}

CONVERSATIONAL_FILES = {
    "conversational/01-CONSTITUTION.md": "docs/pbd/01-constitution.md",
    "conversational/02-BEHAVIOR-SPECS.md": "docs/pbd/02-behavior-specs.md",
    "conversational/03-TEST-SUITE.md": "docs/pbd/03-test-suite.md",
    "conversational/04-MASTER-PROMPT.md": "docs/pbd/04-master-prompt.md",
    "conversational/05-TRACEABILITY.md": "docs/pbd/05-traceability.md",
}

SOFTWARE_FILES = {
    "software/README.md": "README.md",
    "software/AGENTS.md": "AGENTS.md",
    "software/00-PRODUCT-CONTEXT.md": "docs/00-contexto-producto.md",
    "software/01-CONSTITUTION.md": "docs/01-constitution.md",
    "software/02-PRD.md": "docs/02-PRD.md",
    "software/03-SDD.md": "docs/03-SDD.md",
    "software/04-BDD.md": "docs/04-BDD.md",
    "software/05-TDD.md": "docs/05-TDD.md",
    "software/06-TRACEABILITY.md": "docs/06-matriz-trazabilidad.md",
    "software/07-ROADMAP.md": "docs/07-roadmap-entregas.md",
    "software/BOOTSTRAP_CHECKLIST.md": "codex/BOOTSTRAP_CHECKLIST.md",
    "software/CODEX_IMPORT_PROMPT.md": "codex/CODEX_IMPORT_PROMPT.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a governed Humanio CEO project baseline."
    )
    parser.add_argument("--project", required=True, help="Project name.")
    parser.add_argument("--profile", required=True, choices=PROFILES)
    parser.add_argument("--risk", required=True, choices=RISKS)
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination directory. It may exist only if targets do not collide.",
    )
    return parser.parse_args()


def selected_files(profile: str) -> dict[str, str]:
    files = dict(COMMON_FILES)
    if profile in ("software", "hybrid"):
        files.update(SOFTWARE_FILES)
    if profile in ("conversational", "hybrid"):
        files.update(CONVERSATIONAL_FILES)
    return files


def render(content: str, project: str, profile: str, risk: str) -> str:
    return (
        content.replace("{{PROJECT_NAME}}", project)
        .replace("{{PROFILE}}", profile)
        .replace("{{RISK}}", risk)
    )


def main() -> int:
    args = parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    templates_root = plugin_root / "templates"
    output = args.output.resolve()
    file_map = selected_files(args.profile)

    missing_templates = [
        source for source in file_map if not (templates_root / source).is_file()
    ]
    if missing_templates:
        print("ERROR: faltan plantillas del plugin:", file=sys.stderr)
        for path in missing_templates:
            print(f"  - {path}", file=sys.stderr)
        return 2

    collisions = [
        destination for destination in file_map.values() if (output / destination).exists()
    ]
    if collisions:
        print(
            "ERROR: la inicialización se canceló; no se sobrescriben archivos existentes:",
            file=sys.stderr,
        )
        for path in collisions:
            print(f"  - {path}", file=sys.stderr)
        return 3

    created: list[Path] = []
    try:
        for source, destination in file_map.items():
            source_path = templates_root / source
            destination_path = output / destination
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            content = source_path.read_text(encoding="utf-8")
            destination_path.write_text(
                render(content, args.project, args.profile, args.risk),
                encoding="utf-8",
            )
            created.append(destination_path)
    except OSError as error:
        for created_path in reversed(created):
            created_path.unlink(missing_ok=True)
        for directory in sorted(
            {path.parent for path in created}, key=lambda item: len(item.parts), reverse=True
        ):
            try:
                directory.rmdir()
            except OSError:
                pass
        print(f"ERROR: no se pudo completar la inicialización: {error}", file=sys.stderr)
        return 4

    print(
        f"Humanio CEO inicializado: {args.project} "
        f"({args.profile}, {args.risk}) en {output}"
    )
    print(f"Archivos creados: {len(created)}")
    print(f"Siguiente paso: python3 {plugin_root / 'scripts/validate_workspace.py'} {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
