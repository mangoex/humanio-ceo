#!/usr/bin/env python3
"""Validate a Humanio CEO project with deterministic, dependency-free checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


PROFILES = ("conversational", "software", "hybrid")
RISKS = ("R0", "R1", "R2", "R3")
SCAN_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".feature"}

COMMON_REQUIRED = (
    "humanio.yaml",
    "docs/08-registro-riesgos.md",
    "docs/09-registro-cambios.md",
)
CONVERSATIONAL_REQUIRED = (
    "docs/pbd/01-constitution.md",
    "docs/pbd/02-behavior-specs.md",
    "docs/pbd/03-test-suite.md",
    "docs/pbd/04-master-prompt.md",
    "docs/pbd/05-traceability.md",
)
SOFTWARE_REQUIRED = (
    "README.md",
    "AGENTS.md",
    "docs/00-contexto-producto.md",
    "docs/01-constitution.md",
    "docs/02-PRD.md",
    "docs/03-SDD.md",
    "docs/04-BDD.md",
    "docs/05-TDD.md",
    "docs/06-matriz-trazabilidad.md",
    "docs/07-roadmap-entregas.md",
    "codex/BOOTSTRAP_CHECKLIST.md",
    "codex/CODEX_IMPORT_PROMPT.md",
)

SECRET_PATTERNS = (
    re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"']?"
        r"(?!POR CONFIRMAR\b|example\b|changeme\b)([A-Za-z0-9_./+=-]{16,})"
    ),
    re.compile(r"\b(?:sk|ghp|github_pat)_[A-Za-z0-9_=-]{16,}\b"),
)

TRACEABILITY_GROUPS = {
    "conversational": {
        "trace": "docs/pbd/05-traceability.md",
        "sources": (
            "docs/pbd/01-constitution.md",
            "docs/pbd/02-behavior-specs.md",
            "docs/pbd/03-test-suite.md",
        ),
        "patterns": (r"\bBS-RULE-\d{3}\b", r"\bBS-FLOW-\d{3}\b", r"\bPBD-T-\d{3}\b"),
    },
    "software": {
        "trace": "docs/06-matriz-trazabilidad.md",
        "sources": (
            "docs/02-PRD.md",
            "docs/03-SDD.md",
            "docs/04-BDD.md",
            "docs/05-TDD.md",
        ),
        "patterns": (
            r"\bPRD-(?:FR|NFR)-\d{3}\b",
            r"\bSDD-CMP-\d{3}\b",
            r"\bBDD-SC-\d{3}\b",
            r"\bTDD-TC-\d{3}\b",
        ),
    },
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Humanio CEO workspace.")
    parser.add_argument("workspace", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat unresolved placeholders as errors.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    return parser.parse_args()


def parse_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def required_paths(profile: str) -> tuple[str, ...]:
    required = list(COMMON_REQUIRED)
    if profile in ("software", "hybrid"):
        required.extend(SOFTWARE_REQUIRED)
    if profile in ("conversational", "hybrid"):
        required.extend(CONVERSATIONAL_REQUIRED)
    return tuple(required)


def scan_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SCAN_SUFFIXES
        and ".git" not in path.parts
    )


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def validate_traceability(
    root: Path, group_name: str, findings: list[Finding]
) -> None:
    group = TRACEABILITY_GROUPS[group_name]
    trace_path = root / str(group["trace"])
    if not trace_path.is_file():
        return
    trace_content = trace_path.read_text(encoding="utf-8")
    source_content = "\n".join(
        (root / source).read_text(encoding="utf-8")
        for source in group["sources"]
        if (root / source).is_file()
    )
    identifiers: set[str] = set()
    for pattern in group["patterns"]:
        identifiers.update(re.findall(pattern, source_content))
    for identifier in sorted(identifiers):
        if identifier not in trace_content:
            findings.append(
                Finding(
                    "error",
                    "TRACE_MISSING",
                    str(group["trace"]),
                    f"El ID {identifier} no aparece en la matriz de trazabilidad.",
                )
            )


def validate(root: Path, strict: bool) -> tuple[dict[str, str], list[Finding]]:
    findings: list[Finding] = []
    manifest_path = root / "humanio.yaml"
    if not manifest_path.is_file():
        return {}, [
            Finding(
                "error",
                "MANIFEST_MISSING",
                "humanio.yaml",
                "No existe el manifiesto del proyecto.",
            )
        ]

    try:
        manifest = parse_manifest(manifest_path)
    except (OSError, UnicodeError) as error:
        return {}, [
            Finding("error", "MANIFEST_INVALID", "humanio.yaml", str(error))
        ]

    required_keys = ("schema_version", "framework", "framework_version", "project", "profile", "risk")
    for key in required_keys:
        if not manifest.get(key):
            findings.append(
                Finding(
                    "error",
                    "MANIFEST_FIELD",
                    "humanio.yaml",
                    f"Falta el campo obligatorio {key}.",
                )
            )

    profile = manifest.get("profile", "")
    risk = manifest.get("risk", "")
    if profile not in PROFILES:
        findings.append(
            Finding(
                "error",
                "PROFILE_INVALID",
                "humanio.yaml",
                f"Perfil inválido: {profile or '(vacío)'}.",
            )
        )
    if risk not in RISKS:
        findings.append(
            Finding(
                "error",
                "RISK_INVALID",
                "humanio.yaml",
                f"Riesgo inválido: {risk or '(vacío)'}.",
            )
        )
    if manifest.get("framework") != "humanio-ceo":
        findings.append(
            Finding(
                "error",
                "FRAMEWORK_INVALID",
                "humanio.yaml",
                "El campo framework debe ser humanio-ceo.",
            )
        )

    if profile in PROFILES:
        for required in required_paths(profile):
            if not (root / required).is_file():
                findings.append(
                    Finding(
                        "error",
                        "FILE_MISSING",
                        required,
                        "Falta un artefacto obligatorio para el perfil.",
                    )
                )

    for path in scan_files(root):
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(
                Finding("error", "FILE_UNREADABLE", relative(root, path), str(error))
            )
            continue
        unresolved = len(re.findall(r"\bPOR CONFIRMAR\b", content, flags=re.IGNORECASE))
        if unresolved:
            findings.append(
                Finding(
                    "error" if strict else "warning",
                    "PLACEHOLDER",
                    relative(root, path),
                    f"Contiene {unresolved} placeholder(s) sin resolver.",
                )
            )
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                findings.append(
                    Finding(
                        "error",
                        "SECRET_EXPOSED",
                        relative(root, path),
                        "Posible secreto incrustado en un artefacto.",
                    )
                )
                break

    if profile in ("conversational", "hybrid"):
        validate_traceability(root, "conversational", findings)
    if profile in ("software", "hybrid"):
        validate_traceability(root, "software", findings)
    return manifest, findings


def main() -> int:
    args = parse_args()
    root = args.workspace.resolve()
    if not root.is_dir():
        print(f"ERROR: el workspace no existe o no es directorio: {root}", file=sys.stderr)
        return 2

    manifest, findings = validate(root, args.strict)
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    payload = {
        "workspace": str(root),
        "profile": manifest.get("profile"),
        "risk": manifest.get("risk"),
        "strict": args.strict,
        "valid": errors == 0,
        "errors": errors,
        "warnings": warnings,
        "findings": [asdict(item) for item in findings],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item.severity.upper()} [{item.code}] {item.path}: {item.message}")
        print(
            f"Resultado: {'VÁLIDO' if errors == 0 else 'INVÁLIDO'} "
            f"({errors} errores, {warnings} advertencias)"
        )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
