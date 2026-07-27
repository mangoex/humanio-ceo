#!/usr/bin/env python3
"""Portable, reversible project adapters for Humanio CEO."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = Path(".humanio/integrations.json")
START_MARKER = "<!-- humanio-ceo:managed:start -->"
END_MARKER = "<!-- humanio-ceo:managed:end -->"
ADAPTERS = ("generic", "codex", "cursor", "claude", "copilot", "gemini")
TARGETS = {
    "generic": Path(".humanio/README.md"),
    "codex": Path("AGENTS.md"),
    "cursor": Path("AGENTS.md"),
    "claude": Path("CLAUDE.md"),
    "copilot": Path(".github/copilot-instructions.md"),
    "gemini": Path("GEMINI.md"),
}
SIGNALS = {
    "codex": (Path(".codex"),),
    "cursor": (Path(".cursor"),),
    "claude": (Path(".claude"), Path("CLAUDE.md")),
    "copilot": (
        Path(".github/copilot-instructions.md"),
        Path(".github/instructions"),
    ),
    "gemini": (Path(".gemini"), Path("GEMINI.md")),
}


class AdapterError(RuntimeError):
    """Raised when an adapter operation cannot be completed safely."""


@dataclass(frozen=True)
class Change:
    path: Path
    action: str


def framework_version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def detect(workspace: Path) -> list[str]:
    """Return adapters backed by explicit repository signals."""
    root = workspace.resolve()
    if not root.is_dir():
        raise AdapterError(f"el workspace no existe o no es directorio: {root}")
    found = ["generic"]
    for adapter, signals in SIGNALS.items():
        if any((root / signal).exists() for signal in signals):
            found.append(adapter)
    return found


def resolve_adapters(requested: Iterable[str], workspace: Path) -> list[str]:
    values = list(requested)
    if not values:
        values = ["auto"]
    unknown = sorted(set(values) - set(ADAPTERS) - {"auto", "all"})
    if unknown:
        raise AdapterError(f"adaptadores desconocidos: {', '.join(unknown)}")
    selected: set[str] = set()
    for value in values:
        if value == "auto":
            selected.update(detect(workspace))
        elif value == "all":
            selected.update(ADAPTERS)
        else:
            selected.add(value)
    return [adapter for adapter in ADAPTERS if adapter in selected]


def instruction_body(target: Path, adapters: list[str]) -> str:
    if target == TARGETS["generic"]:
        return """# Integración Humanio CEO

Este directorio registra la integración portable del proyecto. La fuente de
gobierno permanece en `humanio.yaml`, `docs/` y los artefactos trazables del
repositorio.

Comandos principales:

```bash
humanio validate . --strict
humanio status .
humanio sync .
```
"""
    labels = ", ".join(adapters)
    return f"""## Humanio CEO

Integración activa para: {labels}.

Este proyecto está gobernado por Humanio CEO Engineering Framework.

1. Leer `humanio.yaml` y la documentación aplicable antes de modificar código o prompts.
2. Respetar este orden: Constitución; decisiones confirmadas y ADR vigentes;
   requisitos; diseño; BDD y TDD; planes; implementación.
3. Distinguir información confirmada, inferida, pendiente y contradictoria.
4. Propagar cambios desde la fuente de mayor autoridad y mantener IDs y trazabilidad.
5. No afirmar pruebas ni readiness sin evidencia ejecutada.
6. Ejecutar `humanio validate . --strict` antes de cerrar un incremento.
"""


def managed_block(target: Path, adapters: list[str]) -> str:
    body = instruction_body(target, adapters).rstrip()
    return f"{START_MARKER}\n{body}\n{END_MARKER}\n"


def marker_bounds(content: str, path: Path) -> tuple[int, int] | None:
    starts = content.count(START_MARKER)
    ends = content.count(END_MARKER)
    if starts == 0 and ends == 0:
        return None
    if starts != 1 or ends != 1:
        raise AdapterError(
            f"{path}: marcas Humanio incompletas o duplicadas; no se escribió nada"
        )
    start = content.index(START_MARKER)
    end_start = content.find(END_MARKER, start)
    if end_start < 0:
        raise AdapterError(f"{path}: orden inválido de marcas Humanio")
    end = end_start + len(END_MARKER)
    if content[end : end + 2] == "\r\n":
        end += 2
    elif content[end : end + 1] == "\n":
        end += 1
    return start, end


def put_block(content: str, block: str, path: Path) -> str:
    bounds = marker_bounds(content, path)
    if bounds is None:
        return f"{content}{block}"
    start, end = bounds
    return f"{content[:start]}{block}{content[end:]}"


def remove_block(content: str, path: Path) -> str:
    bounds = marker_bounds(content, path)
    if bounds is None:
        return content
    start, end = bounds
    return f"{content[:start]}{content[end:]}"


def target_map(adapters: Iterable[str]) -> dict[Path, list[str]]:
    mapping: dict[Path, list[str]] = {}
    for adapter in ADAPTERS:
        if adapter in adapters:
            mapping.setdefault(TARGETS[adapter], []).append(adapter)
    return mapping


def ensure_workspace(workspace: Path) -> Path:
    root = workspace.resolve()
    if not root.is_dir():
        raise AdapterError(f"el workspace no existe o no es directorio: {root}")
    manifest = root / "humanio.yaml"
    if not manifest.is_file():
        raise AdapterError(
            f"falta {manifest}; inicialice o adopte el proyecto antes de integrarlo"
        )
    return root


def safe_path(root: Path, relative: Path) -> Path:
    path = root / relative
    parent = root
    for part in relative.parts[:-1]:
        parent = parent / part
        if parent.is_symlink():
            raise AdapterError(
                f"no se administran rutas bajo enlaces simbólicos: {parent}"
            )
    if path.is_symlink():
        raise AdapterError(f"no se administran enlaces simbólicos: {path}")
    return path


def load_state(root: Path, required: bool = False) -> dict[str, object]:
    path = safe_path(root, STATE_PATH)
    if not path.exists():
        if required:
            raise AdapterError("el proyecto no tiene una integración Humanio instalada")
        return {
            "schema_version": 1,
            "framework_version": framework_version(),
            "adapters": [],
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AdapterError(f"estado de integración inválido: {error}") from error
    if not isinstance(data, dict):
        raise AdapterError("estado de integración inválido: se esperaba un objeto JSON")
    adapters = data.get("adapters")
    targets = data.get("targets")
    if (
        data.get("schema_version") != 1
        or not isinstance(adapters, list)
        or any(adapter not in ADAPTERS for adapter in adapters)
        or len(adapters) != len(set(adapters))
        or adapters != [adapter for adapter in ADAPTERS if adapter in adapters]
        or not isinstance(targets, dict)
    ):
        raise AdapterError("estado de integración incompatible o corrupto")
    expected_targets = target_map(adapters)
    if set(targets) != {path.as_posix() for path in expected_targets}:
        raise AdapterError("el inventario de destinos del estado es inválido")
    for path, values in expected_targets.items():
        entry = targets[path.as_posix()]
        if (
            not isinstance(entry, dict)
            or entry.get("adapters") != values
            or not isinstance(entry.get("block_sha256"), str)
            or len(entry["block_sha256"]) != 64
        ):
            raise AdapterError(f"estado inválido para el destino {path.as_posix()}")
    return data


def read_target(path: Path) -> str:
    if path.is_symlink():
        raise AdapterError(f"no se administran enlaces simbólicos: {path}")
    if not path.exists():
        return ""
    if not path.is_file():
        raise AdapterError(f"el destino no es un archivo regular: {path}")
    return path.read_text(encoding="utf-8")


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.humanio-", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        temporary.chmod(mode)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def desired_state(adapters: list[str], mapping: dict[Path, list[str]]) -> str:
    targets = {
        path.as_posix(): {
            "adapters": values,
            "block_sha256": sha256_text(managed_block(path, values)),
        }
        for path, values in sorted(mapping.items(), key=lambda item: item[0].as_posix())
    }
    payload = {
        "schema_version": 1,
        "framework_version": framework_version(),
        "adapters": adapters,
        "targets": targets,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def apply_contents(
    root: Path, desired: dict[Path, str | None], state: str | None, dry_run: bool
) -> list[Change]:
    originals: dict[Path, str | None] = {}
    changes: list[Change] = []
    all_desired = dict(desired)
    all_desired[STATE_PATH] = state

    for relative, content in all_desired.items():
        path = safe_path(root, relative)
        current = read_target(path) if path.exists() else None
        originals[relative] = current
        if content == current:
            continue
        action = "remove" if content is None else ("create" if current is None else "update")
        changes.append(Change(relative, action))

    if dry_run:
        return changes

    written: list[Path] = []
    try:
        for change in changes:
            path = root / change.path
            content = all_desired[change.path]
            if content is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, content)
            written.append(change.path)
    except OSError as error:
        for relative in reversed(written):
            path = root / relative
            original = originals[relative]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, original)
        raise AdapterError(f"la operación fue revertida tras un fallo de escritura: {error}") from error
    prune_empty_directories(root)
    return changes


def prune_empty_directories(root: Path) -> None:
    candidates = (root / ".humanio",)
    for directory in candidates:
        try:
            directory.rmdir()
        except OSError:
            pass


def install(
    workspace: Path, requested: Iterable[str], dry_run: bool = False
) -> tuple[list[str], list[Change]]:
    root = ensure_workspace(workspace)
    state = load_state(root)
    existing = state["adapters"]
    assert isinstance(existing, list)
    selected = resolve_adapters(requested, root)
    adapters = [adapter for adapter in ADAPTERS if adapter in set(existing) | set(selected)]
    mapping = target_map(adapters)

    desired: dict[Path, str | None] = {}
    for relative, values in mapping.items():
        path = safe_path(root, relative)
        current = read_target(path)
        desired[relative] = put_block(current, managed_block(relative, values), path)

    changes = apply_contents(root, desired, desired_state(adapters, mapping), dry_run)
    return adapters, changes


def sync(workspace: Path, dry_run: bool = False) -> tuple[list[str], list[Change]]:
    root = ensure_workspace(workspace)
    state = load_state(root, required=True)
    adapters = state["adapters"]
    assert isinstance(adapters, list)
    mapping = target_map(adapters)
    desired: dict[Path, str | None] = {}
    for relative, values in mapping.items():
        path = safe_path(root, relative)
        current = read_target(path)
        desired[relative] = put_block(current, managed_block(relative, values), path)
    changes = apply_contents(root, desired, desired_state(adapters, mapping), dry_run)
    return adapters, changes


def uninstall(
    workspace: Path, requested: Iterable[str], dry_run: bool = False
) -> tuple[list[str], list[Change]]:
    root = ensure_workspace(workspace)
    state = load_state(root, required=True)
    existing = state["adapters"]
    assert isinstance(existing, list)
    values = list(requested)
    selected = existing if not values or "all" in values else resolve_adapters(values, root)
    missing = sorted(set(selected) - set(existing))
    if missing:
        raise AdapterError(f"adaptadores no instalados: {', '.join(missing)}")
    adapters = [adapter for adapter in existing if adapter not in set(selected)]
    old_mapping = target_map(existing)
    new_mapping = target_map(adapters)
    desired: dict[Path, str | None] = {}
    for relative, old_values in old_mapping.items():
        path = safe_path(root, relative)
        current = read_target(path)
        if relative in new_mapping:
            desired[relative] = put_block(
                current,
                managed_block(relative, new_mapping[relative]),
                path,
            )
        else:
            cleaned = remove_block(current, path)
            desired[relative] = cleaned if cleaned.strip() else None
    state_content = desired_state(adapters, new_mapping) if adapters else None
    changes = apply_contents(root, desired, state_content, dry_run)
    return adapters, changes


def status(workspace: Path) -> dict[str, object]:
    root = ensure_workspace(workspace)
    state = load_state(root)
    adapters = state["adapters"]
    assert isinstance(adapters, list)
    mapping = target_map(adapters)
    targets: dict[str, str] = {}
    healthy = True
    for relative, values in mapping.items():
        path = safe_path(root, relative)
        try:
            current = read_target(path)
            expected = managed_block(relative, values)
            bounds = marker_bounds(current, path)
            state_targets = state.get("targets")
            assert isinstance(state_targets, dict)
            recorded = state_targets[relative.as_posix()]
            assert isinstance(recorded, dict)
            valid = (
                bounds is not None
                and current[bounds[0] : bounds[1]] == expected
                and recorded.get("block_sha256") == sha256_text(expected)
            )
        except AdapterError:
            valid = False
        targets[relative.as_posix()] = "ok" if valid else "drift"
        healthy = healthy and valid
    return {
        "workspace": str(root),
        "framework_version": state.get("framework_version"),
        "adapters": adapters,
        "targets": targets,
        "healthy": healthy and state.get("framework_version") == framework_version(),
    }
