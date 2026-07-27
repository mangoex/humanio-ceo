from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "scripts/package_plugin.py"
INSTALL = ROOT / "scripts/install_plugin.py"
VERIFY_EVIDENCE = ROOT / "scripts/verify_official_evidence.py"
OFFICIAL_EVIDENCE = (
    ROOT / "pilots/humanio-ceo/evidence/official-validation.json"
)
VERIFY_SPEC = importlib.util.spec_from_file_location(
    "verify_official_evidence", VERIFY_EVIDENCE
)
if VERIFY_SPEC is None or VERIFY_SPEC.loader is None:
    raise RuntimeError("No se pudo cargar verify_official_evidence.py")
VERIFY_MODULE = importlib.util.module_from_spec(VERIFY_SPEC)
VERIFY_SPEC.loader.exec_module(VERIFY_MODULE)


class ReleaseTests(unittest.TestCase):
    def run_script(self, script: Path, *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *(str(arg) for arg in args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_package_is_deterministic_and_auditable(self) -> None:
        """TDD-TC-004: package bytes are reproducible and include audit inputs."""
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.zip"
            second = Path(temporary) / "second.zip"
            self.assertEqual(
                self.run_script(PACKAGE, "--output", first).returncode, 0
            )
            self.assertEqual(
                self.run_script(PACKAGE, "--output", second).returncode, 0
            )
            self.assertEqual(
                hashlib.sha256(first.read_bytes()).digest(),
                hashlib.sha256(second.read_bytes()).digest(),
            )
            with zipfile.ZipFile(first) as archive:
                names = set(archive.namelist())
            self.assertIn("humanio-ceo/.codex-plugin/plugin.json", names)
            self.assertIn(
                "humanio-ceo/skills/humanio-project-engineer/SKILL.md", names
            )
            self.assertIn("humanio-ceo/pilots/humanio-ceo/EVIDENCE.md", names)
            self.assertIn("humanio-ceo/tests/evals/readiness-cases.json", names)
            self.assertIn(
                "humanio-ceo/tests/fixtures/software/humanio.yaml", names
            )
            self.assertIn("humanio-ceo/.github/workflows/validate.yml", names)
            self.assertFalse(any("__pycache__" in name for name in names))
            hidden_name = ".hidden-unvalidated-skill"
            hidden_root = ROOT / "skills" / hidden_name
            hidden_root.mkdir()
            try:
                (hidden_root / "SKILL.md").write_text(
                    "---\nname: hidden\ndescription: Must not ship.\n---\n",
                    encoding="utf-8",
                )
                hidden_archive = Path(temporary) / "hidden.zip"
                self.assertEqual(
                    self.run_script(
                        PACKAGE, "--output", hidden_archive
                    ).returncode,
                    0,
                )
                with zipfile.ZipFile(hidden_archive) as archive:
                    hidden_names = set(archive.namelist())
                self.assertFalse(
                    any(f"/skills/{hidden_name}/" in name for name in hidden_names)
                )
            finally:
                (hidden_root / "SKILL.md").unlink(missing_ok=True)
                hidden_root.rmdir()

    def test_local_installer_registers_personal_marketplace(self) -> None:
        """TDD-TC-005: install and update an isolated personal marketplace."""
        with tempfile.TemporaryDirectory() as temporary:
            marketplace_root = Path(temporary) / "plugins-root"
            result = self.run_script(
                INSTALL, "--marketplace-root", marketplace_root
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = (
                marketplace_root
                / "plugins/humanio-ceo/.codex-plugin/plugin.json"
            )
            self.assertTrue(manifest.is_file())
            marketplace = json.loads(
                (marketplace_root / "marketplace.json").read_text(encoding="utf-8")
            )
            self.assertEqual(marketplace["name"], "personal")
            self.assertEqual(marketplace["plugins"][0]["name"], "humanio-ceo")
            repeated = self.run_script(
                INSTALL, "--marketplace-root", marketplace_root
            )
            self.assertEqual(repeated.returncode, 1)
            updated = self.run_script(
                INSTALL, "--marketplace-root", marketplace_root, "--update"
            )
            self.assertEqual(updated.returncode, 0, updated.stdout + updated.stderr)

    def test_official_evidence_matches_current_artifacts(self) -> None:
        result = self.run_script(VERIFY_EVIDENCE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Evidencia oficial vigente", result.stdout)
        skills_root = ROOT / "skills"
        with tempfile.TemporaryDirectory(
            prefix="unvalidated-skill-", dir=skills_root
        ) as temporary:
            (Path(temporary) / "SKILL.md").write_text(
                "---\nname: unvalidated\ndescription: Regression fixture.\n---\n",
                encoding="utf-8",
            )
            rejected = self.run_script(VERIFY_EVIDENCE)
            self.assertEqual(rejected.returncode, 1)
            self.assertIn(
                "installed skills must match the canonical inventory exactly",
                rejected.stderr,
            )
        with tempfile.TemporaryDirectory() as temporary:
            fake_root = Path(temporary)
            fake_contract_root = fake_root / ".codex-plugin"
            fake_contract_root.mkdir()
            (fake_contract_root / "validation-contract.json").write_text(
                (
                    ROOT / ".codex-plugin/validation-contract.json"
                ).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            fake_skills_root = fake_root / "skills"
            fake_skills_root.mkdir()
            required_skills = set(
                VERIFY_MODULE.load_contract(ROOT)["required_skills"]
            )
            for name in sorted(required_skills):
                if name != "traceability-auditor":
                    (fake_skills_root / name).mkdir()
            self.assertNotEqual(
                VERIFY_MODULE.installed_skills(fake_root),
                required_skills,
            )
            payload = json.loads(
                OFFICIAL_EVIDENCE.read_text(encoding="utf-8")
            )
            errors = VERIFY_MODULE.verify(payload, fake_root)
            self.assertTrue(
                any(
                    "installed skills must match the canonical inventory exactly"
                    in error
                    for error in errors
                )
            )
        with tempfile.TemporaryDirectory(
            prefix=".hidden-tooling-", dir=ROOT / "skills"
        ) as temporary:
            (Path(temporary) / "SKILL.md").write_text(
                "---\nname: hidden\ndescription: Ignored metadata fixture.\n---\n",
                encoding="utf-8",
            )
            hidden_ignored = self.run_script(VERIFY_EVIDENCE)
            self.assertEqual(
                hidden_ignored.returncode,
                0,
                hidden_ignored.stdout + hidden_ignored.stderr,
            )


if __name__ == "__main__":
    unittest.main()
