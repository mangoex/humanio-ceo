from __future__ import annotations

import json
import os
import importlib.util
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/humanio.py"
INSTALL_CLI = ROOT / "scripts/install_cli.py"
START_MARKER = "<!-- humanio-ceo:managed:start -->"
END_MARKER = "<!-- humanio-ceo:managed:end -->"


def load_installer_module():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location("install_cli_under_test", INSTALL_CLI)
    if spec is None or spec.loader is None:
        raise RuntimeError("No se pudo cargar install_cli.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CliTestCase(unittest.TestCase):
    def run_script(
        self, script: Path, *args: object
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *(str(arg) for arg in args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def initialize(
        self, workspace: Path, profile: str = "software", adopt: bool = False
    ) -> subprocess.CompletedProcess[str]:
        arguments: list[object] = [
            "init",
            "--project",
            "portable-fixture",
            "--profile",
            profile,
            "--risk",
            "R1",
            "--output",
            workspace,
        ]
        if adopt:
            arguments.append("--adopt")
        return self.run_script(CLI, *arguments)


class PortableCliTests(CliTestCase):
    def test_isolated_cli_install_update_and_uninstall(self) -> None:
        """TDD-TC-006: portable installation works outside the source checkout."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "runtime"
            bin_dir = root / "bin"
            dry_run = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
                "--dry-run",
            )
            self.assertEqual(dry_run.returncode, 0, dry_run.stdout + dry_run.stderr)
            self.assertFalse(destination.exists())
            installed = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
            )
            self.assertEqual(
                installed.returncode, 0, installed.stdout + installed.stderr
            )
            launcher = bin_dir / ("humanio.cmd" if os.name == "nt" else "humanio")
            self.assertTrue(launcher.is_file())
            if os.name != "nt":
                launcher_text = launcher.read_text(encoding="utf-8")
                self.assertTrue(launcher_text.startswith("#!/bin/sh\n"))
                self.assertIn(sys.executable, launcher_text)
            command = (
                ["cmd", "/c", str(launcher), "doctor"]
                if os.name == "nt"
                else [str(launcher), "doctor"]
            )
            doctor = subprocess.run(
                command,
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
            self.assertIn("instalación válida", doctor.stdout)
            repeated = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
            )
            self.assertEqual(repeated.returncode, 1)
            updated = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
                "--update",
            )
            self.assertEqual(updated.returncode, 0, updated.stdout + updated.stderr)
            removed = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
                "--uninstall",
            )
            self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
            self.assertFalse(destination.exists())
            self.assertFalse(launcher.exists())

    def test_foreign_cli_targets_are_never_replaced_or_deleted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "runtime"
            bin_dir = root / "bin"
            destination.mkdir()
            foreign = destination / "keep.txt"
            foreign.write_text("owned by user\n", encoding="utf-8")
            rejected = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
                "--update",
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertTrue(foreign.is_file())
            remove_rejected = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
                "--uninstall",
            )
            self.assertEqual(remove_rejected.returncode, 1)
            self.assertTrue(foreign.is_file())

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "runtime"
            bin_dir = root / "bin"
            bin_dir.mkdir()
            foreign_temporary = bin_dir / ".humanio.tmp"
            foreign_temporary.write_text("owned by user\n", encoding="utf-8")
            installed = self.run_script(
                INSTALL_CLI,
                "--install-root",
                destination,
                "--bin-dir",
                bin_dir,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            self.assertEqual(
                foreign_temporary.read_text(encoding="utf-8"), "owned by user\n"
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "runtime"
            launcher = root / "bin/humanio"
            launcher.parent.mkdir()
            installer = load_installer_module()
            with mock.patch.object(
                installer,
                "write_launcher_atomic",
                side_effect=OSError("simulated launcher failure"),
            ):
                with self.assertRaises(OSError):
                    installer.install(destination, launcher, update=False, dry_run=False)
            self.assertFalse(destination.exists())
            self.assertFalse(launcher.exists())


class AdapterIntegrationTests(CliTestCase):
    def test_integrate_sync_and_uninstall_preserve_user_content(self) -> None:
        """TDD-TC-007: adapters are idempotent, selective, and reversible."""
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "project"
            workspace.mkdir()
            readme = workspace / "README.md"
            agents = workspace / "AGENTS.md"
            readme.write_text("# Producto existente\n", encoding="utf-8")
            original_agents = "# Reglas del equipo con corte  \n\n"
            agents.write_text(original_agents, encoding="utf-8")
            if os.name != "nt":
                agents.chmod(0o640)
            initialized = self.initialize(workspace, adopt=True)
            self.assertEqual(
                initialized.returncode,
                0,
                initialized.stdout + initialized.stderr,
            )
            self.assertEqual(readme.read_text(encoding="utf-8"), "# Producto existente\n")
            self.assertEqual(agents.read_text(encoding="utf-8"), original_agents)

            integrated = self.run_script(
                CLI, "install", workspace, "--adapter", "all"
            )
            self.assertEqual(
                integrated.returncode,
                0,
                integrated.stdout + integrated.stderr,
            )
            state_path = workspace / ".humanio/integrations.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(
                state["adapters"],
                ["generic", "codex", "cursor", "claude", "copilot", "gemini"],
            )
            self.assertIn("# Reglas del equipo", agents.read_text(encoding="utf-8"))
            self.assertEqual(agents.read_text(encoding="utf-8").count(START_MARKER), 1)
            if os.name != "nt":
                self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o640)

            claude = workspace / "CLAUDE.md"
            claude.write_text(
                claude.read_text(encoding="utf-8") + "\n# Nota del usuario\n",
                encoding="utf-8",
            )
            synced = self.run_script(CLI, "sync", workspace)
            self.assertEqual(synced.returncode, 0, synced.stdout + synced.stderr)
            self.assertIn("# Nota del usuario", claude.read_text(encoding="utf-8"))
            second_sync = self.run_script(CLI, "sync", workspace)
            self.assertEqual(second_sync.returncode, 0)
            self.assertIn("sin cambios", second_sync.stdout)

            remove_cursor = self.run_script(
                CLI, "uninstall", workspace, "--adapter", "cursor"
            )
            self.assertEqual(
                remove_cursor.returncode,
                0,
                remove_cursor.stdout + remove_cursor.stderr,
            )
            agents_content = agents.read_text(encoding="utf-8")
            self.assertIn("Integración activa para: codex.", agents_content)
            self.assertNotIn("codex, cursor", agents_content)

            removed = self.run_script(CLI, "uninstall", workspace)
            self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
            self.assertEqual(agents.read_text(encoding="utf-8"), original_agents)
            self.assertEqual(readme.read_text(encoding="utf-8"), "# Producto existente\n")
            self.assertIn("# Nota del usuario", claude.read_text(encoding="utf-8"))
            self.assertNotIn(START_MARKER, claude.read_text(encoding="utf-8"))
            self.assertFalse(state_path.exists())

    def test_malformed_markers_abort_without_writes(self) -> None:
        """TDD-TC-008: malformed markers abort the complete operation."""
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "project"
            initialized = self.initialize(workspace, profile="conversational")
            self.assertEqual(initialized.returncode, 0)
            agents = workspace / "AGENTS.md"
            original = f"# Existing\n{START_MARKER}\n"
            agents.write_text(original, encoding="utf-8")
            result = self.run_script(CLI, "install", workspace, "--adapter", "all")
            self.assertEqual(result.returncode, 1)
            self.assertIn("marcas Humanio incompletas", result.stderr)
            self.assertEqual(agents.read_text(encoding="utf-8"), original)
            self.assertFalse((workspace / ".humanio").exists())
            self.assertFalse((workspace / "CLAUDE.md").exists())

    def test_reversed_markers_and_symlinked_parents_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "project"
            initialized = self.initialize(workspace, profile="conversational")
            self.assertEqual(initialized.returncode, 0)
            agents = workspace / "AGENTS.md"
            agents.write_text(
                f"{END_MARKER}\ncontenido\n{START_MARKER}\n", encoding="utf-8"
            )
            reversed_result = self.run_script(
                CLI, "install", workspace, "--adapter", "codex"
            )
            self.assertEqual(reversed_result.returncode, 1)
            self.assertIn("orden inválido", reversed_result.stderr)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "project"
            initialized = self.initialize(workspace, profile="conversational")
            self.assertEqual(initialized.returncode, 0)
            external = root / "external"
            external.mkdir()
            try:
                (workspace / ".github").symlink_to(external, target_is_directory=True)
            except OSError:
                self.skipTest("el sistema no permite crear enlaces simbólicos")
            symlinked = self.run_script(
                CLI, "install", workspace, "--adapter", "copilot"
            )
            self.assertEqual(symlinked.returncode, 1)
            self.assertIn("enlaces simbólicos", symlinked.stderr)
            self.assertFalse((external / "copilot-instructions.md").exists())

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "project"
            workspace.mkdir()
            outside = root / "outside-readme.md"
            try:
                (workspace / "README.md").symlink_to(outside)
            except OSError:
                self.skipTest("el sistema no permite crear enlaces simbólicos")
            adopted = self.initialize(workspace, adopt=True)
            self.assertEqual(adopted.returncode, 3)
            self.assertIn("enlaces simbólicos", adopted.stderr)
            self.assertFalse(outside.exists())
            self.assertFalse((workspace / "humanio.yaml").exists())

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "project"
            workspace.mkdir()
            outside_docs = root / "outside-docs"
            outside_docs.mkdir()
            try:
                (workspace / "docs").symlink_to(
                    outside_docs, target_is_directory=True
                )
            except OSError:
                self.skipTest("el sistema no permite crear enlaces simbólicos")
            adopted = self.initialize(workspace, adopt=True)
            self.assertEqual(adopted.returncode, 3)
            self.assertIn("enlaces simbólicos", adopted.stderr)
            self.assertEqual(list(outside_docs.iterdir()), [])

    def test_auto_detection_and_dry_run(self) -> None:
        """TDD-TC-009: auto uses explicit signals and dry-run performs no writes."""
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "project"
            initialized = self.initialize(workspace, profile="conversational")
            self.assertEqual(initialized.returncode, 0)
            (workspace / ".cursor").mkdir()
            (workspace / ".claude").mkdir()
            (workspace / "GEMINI.md").write_text("# Gemini\n", encoding="utf-8")
            detected = self.run_script(CLI, "detect", workspace, "--json")
            self.assertEqual(detected.returncode, 0)
            payload = json.loads(detected.stdout)
            self.assertEqual(
                payload["adapters"], ["generic", "cursor", "claude", "gemini"]
            )
            dry_run = self.run_script(
                CLI, "install", workspace, "--adapter", "auto", "--dry-run"
            )
            self.assertEqual(dry_run.returncode, 0, dry_run.stdout + dry_run.stderr)
            self.assertIn("DRY-RUN", dry_run.stdout)
            self.assertFalse((workspace / ".humanio").exists())
            self.assertEqual(
                (workspace / "GEMINI.md").read_text(encoding="utf-8"), "# Gemini\n"
            )

    def test_status_detects_and_sync_repairs_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "project"
            self.assertEqual(
                self.initialize(workspace, profile="conversational").returncode, 0
            )
            self.assertEqual(
                self.run_script(
                    CLI, "install", workspace, "--adapter", "claude"
                ).returncode,
                0,
            )
            claude = workspace / "CLAUDE.md"
            content = claude.read_text(encoding="utf-8")
            claude.write_text(
                content.replace("No afirmar pruebas", "Afirmar pruebas"),
                encoding="utf-8",
            )
            status = self.run_script(CLI, "status", workspace, "--json")
            self.assertEqual(status.returncode, 1)
            self.assertFalse(json.loads(status.stdout)["healthy"])
            self.assertEqual(self.run_script(CLI, "sync", workspace).returncode, 0)
            repaired = self.run_script(CLI, "status", workspace, "--json")
            self.assertEqual(repaired.returncode, 0)
            self.assertTrue(json.loads(repaired.stdout)["healthy"])
            (workspace / ".humanio/integrations.json").write_text(
                "[]\n", encoding="utf-8"
            )
            invalid = self.run_script(CLI, "status", workspace)
            self.assertEqual(invalid.returncode, 1)
            self.assertIn("se esperaba un objeto JSON", invalid.stderr)
            self.assertNotIn("Traceback", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
