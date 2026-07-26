from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "scripts/init_project.py"
VALIDATE = ROOT / "scripts/validate_workspace.py"


class FrameworkFlowTests(unittest.TestCase):
    def run_script(self, script: Path, *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *(str(arg) for arg in args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def initialize(self, root: Path, profile: str, risk: str = "R1") -> Path:
        workspace = root / profile
        result = self.run_script(
            INIT,
            "--project",
            f"fixture-{profile}",
            "--profile",
            profile,
            "--risk",
            risk,
            "--output",
            workspace,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return workspace

    def test_each_profile_initializes_and_passes_normal_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for profile in ("conversational", "software", "hybrid"):
                with self.subTest(profile=profile):
                    workspace = self.initialize(root, profile)
                    result = self.run_script(VALIDATE, workspace)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn("VÁLIDO", result.stdout)

    def test_hybrid_contains_both_artifact_families(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self.initialize(Path(temporary), "hybrid", "R2")
            self.assertTrue((workspace / "docs/02-PRD.md").is_file())
            self.assertTrue((workspace / "docs/pbd/02-behavior-specs.md").is_file())
            manifest = (workspace / "humanio.yaml").read_text(encoding="utf-8")
            self.assertIn("profile: \"hybrid\"", manifest)
            self.assertIn("risk: \"R2\"", manifest)

    def test_strict_validation_rejects_unresolved_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self.initialize(Path(temporary), "software")
            result = self.run_script(VALIDATE, "--strict", workspace)
            self.assertEqual(result.returncode, 1)
            self.assertIn("[PLACEHOLDER]", result.stdout)

    def test_initializer_never_overwrites_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = self.initialize(root, "conversational")
            manifest = workspace / "humanio.yaml"
            before = manifest.read_text(encoding="utf-8")
            result = self.run_script(
                INIT,
                "--project",
                "replacement",
                "--profile",
                "conversational",
                "--risk",
                "R3",
                "--output",
                workspace,
            )
            self.assertEqual(result.returncode, 3)
            self.assertEqual(manifest.read_text(encoding="utf-8"), before)
            self.assertIn("no se sobrescriben", result.stderr)

    def test_validator_detects_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self.initialize(Path(temporary), "software")
            (workspace / "docs/02-PRD.md").unlink()
            result = self.run_script(VALIDATE, "--json", workspace)
            self.assertEqual(result.returncode, 1)
            self.assertIn('"code": "FILE_MISSING"', result.stdout)


if __name__ == "__main__":
    unittest.main()
