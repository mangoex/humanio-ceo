#!/usr/bin/env python3
"""Install the portable Humanio CLI into an isolated user prefix."""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import sys
import tempfile
from pathlib import Path

from package_plugin import ROOT, plugin_files


LAUNCHER_MARKER = "humanio-ceo portable launcher"
INSTALL_MARKER = ".humanio-cli-installation"


def default_paths() -> tuple[Path, Path]:
    if os.name == "nt":
        local = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
        return local / "Humanio/humanio-ceo", local / "Humanio/bin"
    return Path.home() / ".local/share/humanio-ceo", Path.home() / ".local/bin"


def parse_args() -> argparse.Namespace:
    install_root, bin_dir = default_paths()
    parser = argparse.ArgumentParser(description="Install the portable Humanio CLI.")
    parser.add_argument("--install-root", type=Path, default=install_root)
    parser.add_argument("--bin-dir", type=Path, default=bin_dir)
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def launcher_path(bin_dir: Path) -> Path:
    return bin_dir / ("humanio.cmd" if os.name == "nt" else "humanio")


def launcher_content(destination: Path) -> str:
    script = destination / "scripts/humanio.py"
    if os.name == "nt":
        return (
            f"@rem {LAUNCHER_MARKER}\r\n"
            f'@"{sys.executable}" "{script}" %*\r\n'
        )
    return (
        "#!/bin/sh\n"
        f"# {LAUNCHER_MARKER}\n"
        f"exec {shlex.quote(sys.executable)} {shlex.quote(str(script))} \"$@\"\n"
    )


def write_launcher_atomic(launcher: Path, content: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{launcher.name}.humanio-", dir=launcher.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
        if os.name != "nt":
            temporary.chmod(0o755)
        temporary.replace(launcher)
    finally:
        temporary.unlink(missing_ok=True)


def validate_targets(destination: Path, launcher: Path, update: bool) -> None:
    if destination.is_symlink() or launcher.is_symlink():
        raise OSError("la instalación y el lanzador no pueden ser enlaces simbólicos")
    if destination.exists() and not update:
        raise FileExistsError(
            f"ya existe {destination}; use --update para reemplazarla"
        )
    if destination.exists() and not (
        destination.is_dir()
        and (destination / INSTALL_MARKER).is_file()
        and LAUNCHER_MARKER
        in (destination / INSTALL_MARKER).read_text(encoding="utf-8")
    ):
        raise FileExistsError(
            f"se rechazó reemplazar un directorio ajeno a Humanio: {destination}"
        )
    if launcher.exists():
        content = launcher.read_text(encoding="utf-8")
        if LAUNCHER_MARKER not in content:
            raise FileExistsError(
                f"ya existe un lanzador ajeno a Humanio: {launcher}"
            )
        if not update and not destination.exists():
            raise FileExistsError(
                f"ya existe {launcher}; use --update para repararlo"
            )


def copy_runtime(staging: Path) -> None:
    for source in plugin_files():
        relative = source.relative_to(ROOT)
        target = staging / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    (staging / INSTALL_MARKER).write_text(
        f"{LAUNCHER_MARKER}\nversion={version}\n", encoding="utf-8"
    )


def install(
    destination: Path, launcher: Path, update: bool, dry_run: bool
) -> list[str]:
    validate_targets(destination, launcher, update)
    actions = [
        f"{'actualizar' if destination.exists() else 'crear'} {destination}",
        f"{'actualizar' if launcher.exists() else 'crear'} {launcher}",
    ]
    if dry_run:
        return actions

    destination.parent.mkdir(parents=True, exist_ok=True)
    launcher.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=".humanio-cli-", dir=str(destination.parent))
    )
    backup = destination.with_name(f".{destination.name}.backup")
    previous_launcher = (
        launcher.read_text(encoding="utf-8") if launcher.exists() else None
    )
    had_destination = destination.exists()
    try:
        copy_runtime(staging)
        if destination.exists():
            if backup.exists():
                raise FileExistsError(f"existe un respaldo pendiente: {backup}")
            destination.rename(backup)
        staging.rename(destination)
        write_launcher_atomic(launcher, launcher_content(destination))
        if backup.exists():
            shutil.rmtree(backup)
    except OSError:
        if destination.exists() and backup.exists():
            shutil.rmtree(destination)
            backup.rename(destination)
        elif backup.exists():
            backup.rename(destination)
        elif not had_destination and destination.exists():
            shutil.rmtree(destination)
        if previous_launcher is None:
            launcher.unlink(missing_ok=True)
        else:
            launcher.write_text(previous_launcher, encoding="utf-8")
        raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return actions


def uninstall(destination: Path, launcher: Path, dry_run: bool) -> list[str]:
    actions: list[str] = []
    if launcher.exists():
        if launcher.is_symlink() or LAUNCHER_MARKER not in launcher.read_text(
            encoding="utf-8"
        ):
            raise OSError(f"se rechazó eliminar un lanzador ajeno: {launcher}")
        actions.append(f"eliminar {launcher}")
    if destination.exists():
        marker = destination / INSTALL_MARKER
        if (
            destination.is_symlink()
            or not destination.is_dir()
            or not marker.is_file()
            or LAUNCHER_MARKER not in marker.read_text(encoding="utf-8")
        ):
            raise OSError(f"se rechazó eliminar un destino inválido: {destination}")
        actions.append(f"eliminar {destination}")
    if dry_run:
        return actions
    launcher.unlink(missing_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    for directory in (launcher.parent, destination.parent):
        try:
            directory.rmdir()
        except OSError:
            pass
    return actions


def main() -> int:
    args = parse_args()
    destination = args.install_root.expanduser().absolute()
    bin_dir = args.bin_dir.expanduser().absolute()
    launcher = launcher_path(bin_dir)
    try:
        if args.uninstall:
            actions = uninstall(destination, launcher, args.dry_run)
        else:
            actions = install(destination, launcher, args.update, args.dry_run)
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    prefix = "DRY-RUN" if args.dry_run else "OK"
    for action in actions:
        print(f"{prefix}: {action}")
    if not args.uninstall:
        print(f"Ejecutable: {launcher}")
        if str(bin_dir) not in os.environ.get("PATH", "").split(os.pathsep):
            print(f"Agregue {bin_dir} a PATH para invocar `humanio` directamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
