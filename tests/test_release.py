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


class ReleaseTests(unittest.TestCase):
    def run_script(self, script: Path, *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *(str(arg) for arg in args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_package_is_deterministic_and_minimal(self) -> None:
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
            self.assertFalse(any("/tests/" in name for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))

    def test_local_installer_registers_personal_marketplace(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
