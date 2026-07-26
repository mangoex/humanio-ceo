from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "scripts/init_project.py"
VALIDATE = ROOT / "scripts/validate_workspace.py"
CLI = ROOT / "scripts/humanio.py"


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

    def test_cli_doctor_and_init(self) -> None:
        doctor = self.run_script(CLI, "doctor")
        self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "cli-project"
            initialized = self.run_script(
                CLI,
                "init",
                "--project",
                "cli-project",
                "--profile",
                "conversational",
                "--risk",
                "R0",
                "--output",
                workspace,
            )
            self.assertEqual(
                initialized.returncode, 0, initialized.stdout + initialized.stderr
            )
            validated = self.run_script(CLI, "validate", workspace)
            self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)

    def test_validator_detects_duplicate_and_undefined_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self.initialize(Path(temporary), "software")
            prd = workspace / "docs/02-PRD.md"
            prd.write_text(
                prd.read_text(encoding="utf-8")
                + "\n### PRD-FR-001\nDuplicado.\n\nReferencia: UNKNOWN-REQ-999\n",
                encoding="utf-8",
            )
            result = self.run_script(VALIDATE, "--json", workspace)
            self.assertEqual(result.returncode, 1)
            self.assertIn('"code": "ID_DUPLICATE"', result.stdout)
            self.assertIn('"code": "ID_UNDEFINED"', result.stdout)

    def test_versioned_fixtures_pass_strict_validation(self) -> None:
        for profile in ("conversational", "software", "hybrid"):
            with self.subTest(profile=profile):
                result = self.run_script(
                    CLI,
                    "validate",
                    ROOT / "tests/fixtures" / profile,
                    "--strict",
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("0 errores, 0 advertencias", result.stdout)

    def test_governed_self_pilot_passes_strict_validation(self) -> None:
        result = self.run_script(
            CLI,
            "validate",
            ROOT / "pilots/humanio-ceo",
            "--strict",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 errores, 0 advertencias", result.stdout)


if __name__ == "__main__":
    unittest.main()
