from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALUATE = ROOT / "scripts/evaluate_readiness.py"
CASES = ROOT / "tests/evals/readiness-cases.json"


class ConversationalEvaluationTests(unittest.TestCase):
    def test_pbd_readiness_gate(self) -> None:
        """PBD-T-001: READY requires every mandatory gate."""
        result = subprocess.run(
            [sys.executable, str(EVALUATE), "--cases", str(CASES)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PBD-T-001 aprobado: 5 casos", result.stdout)
        valid_cases = json.loads(CASES.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            for name, cases in (
                ("empty", []),
                ("incomplete", valid_cases[:-1]),
            ):
                with self.subTest(name=name):
                    path = Path(temporary) / f"{name}.json"
                    path.write_text(json.dumps(cases), encoding="utf-8")
                    rejected = subprocess.run(
                        [sys.executable, str(EVALUATE), "--cases", str(path)],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(rejected.returncode, 2)
                    self.assertIn(
                        "se requiere el conjunto completo",
                        rejected.stderr,
                    )


if __name__ == "__main__":
    unittest.main()
