#!/usr/bin/env python3
"""Build a deterministic Humanio CEO plugin archive."""

from __future__ import annotations

import argparse
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = (
    ".codex-plugin",
    "docs",
    "pilots",
    "schemas",
    "scripts",
    "skills",
    "templates",
    "tests",
)
ROOT_FILES = (
    ".github/workflows/validate.yml",
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
    "VERSION",
)
EXCLUDED_PARTS = {"__pycache__", ".git"}
ALLOWED_HIDDEN_ROOTS = {".codex-plugin", ".github"}


def is_excluded(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if EXCLUDED_PARTS.intersection(relative.parts) or path.suffix == ".pyc":
        return True
    return any(
        part.startswith(".")
        and not (index == 0 and part in ALLOWED_HIDDEN_ROOTS)
        for index, part in enumerate(relative.parts)
    )


def plugin_files() -> list[Path]:
    files = [ROOT / path for path in ROOT_FILES]
    for directory in DIRECTORIES:
        files.extend(path for path in (ROOT / directory).rglob("*") if path.is_file())
    return sorted(
        path
        for path in files
        if not is_excluded(path)
    )


def parse_args() -> argparse.Namespace:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    parser = argparse.ArgumentParser(description="Package the Humanio CEO plugin.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / f"humanio-ceo-{version}.zip",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def build(output: Path, force: bool = False) -> Path:
    output = output.resolve()
    if output.exists() and not force:
        raise FileExistsError(f"El archivo ya existe: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in plugin_files():
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"humanio-ceo/{relative}", (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if path.suffix == ".py" else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            archive.writestr(info, path.read_bytes())
    return output


def main() -> int:
    args = parse_args()
    try:
        output = build(args.output, args.force)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 1
    print(f"Paquete creado: {output}")
    print(f"Archivos: {len(plugin_files())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
