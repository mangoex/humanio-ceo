#!/usr/bin/env python3
"""Install Humanio CEO into a local Codex personal marketplace."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

from package_plugin import ROOT, plugin_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Humanio CEO locally.")
    parser.add_argument(
        "--marketplace-root",
        type=Path,
        default=Path.home() / ".agents" / "plugins",
    )
    parser.add_argument("--update", action="store_true")
    return parser.parse_args()


def copy_plugin(destination: Path, update: bool) -> None:
    if ROOT.resolve() == destination.resolve():
        return
    if destination.exists() and not update:
        raise FileExistsError(
            f"Ya existe {destination}. Use --update para reemplazar esa instalación."
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=".humanio-ceo-", dir=str(destination.parent))
    )
    try:
        for source in plugin_files():
            relative = source.relative_to(ROOT)
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        if destination.exists():
            backup = destination.with_name(".humanio-ceo-backup")
            if backup.exists():
                shutil.rmtree(backup)
            destination.rename(backup)
            staging.rename(destination)
            shutil.rmtree(backup)
        else:
            staging.rename(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def register_marketplace(root: Path) -> str:
    marketplace_path = root / "marketplace.json"
    if marketplace_path.exists():
        data = json.loads(marketplace_path.read_text(encoding="utf-8"))
    else:
        data = {
            "name": "personal",
            "interface": {"displayName": "Personal"},
            "plugins": [],
        }
    name = data.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("El marketplace no tiene un nombre válido.")
    plugins = data.setdefault("plugins", [])
    expected = {
        "name": "humanio-ceo",
        "source": {"source": "local", "path": "./plugins/humanio-ceo"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }
    matches = [entry for entry in plugins if entry.get("name") == "humanio-ceo"]
    if matches and matches[0].get("source") != expected["source"]:
        raise ValueError("Ya existe humanio-ceo apuntando a otra fuente.")
    if not matches:
        plugins.append(expected)
    root.mkdir(parents=True, exist_ok=True)
    temporary = marketplace_path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(marketplace_path)
    return name


def main() -> int:
    args = parse_args()
    marketplace_root = args.marketplace_root.resolve()
    destination = marketplace_root / "plugins" / "humanio-ceo"
    try:
        copy_plugin(destination, args.update)
        marketplace_name = register_marketplace(marketplace_root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Humanio CEO instalado en {destination}")
    print(f"Activar con: codex plugin add humanio-ceo@{marketplace_name}")
    print("Abrir un hilo nuevo después de activarlo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
