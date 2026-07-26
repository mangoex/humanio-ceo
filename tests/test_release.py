from __future__ import annotations

import hashlib
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
            self.assertIn("humanio-ceo/.github/workflows/validate.yml", names)
            self.assertFalse(any("__pycache__" in name for name in names))

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


if __name__ == "__main__":
    unittest.main()
