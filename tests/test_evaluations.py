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
        altered_cases = [dict(case) for case in valid_cases]
        altered_cases[0].update(
            strict_exit_code=0,
            expected="READY",
        )
        type_altered_cases = [dict(case) for case in valid_cases]
        type_altered_cases[0]["tests_passed"] = 1
        with tempfile.TemporaryDirectory() as temporary:
            for name, cases in (
                ("empty", []),
                ("incomplete", valid_cases[:-1]),
                ("altered-semantics", altered_cases),
                ("altered-types", type_altered_cases),
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
                    self.assertTrue(
                        "se requiere el conjunto completo" in rejected.stderr
                        or "no coincide con su escenario canónico" in rejected.stderr
                        or "contiene campos o tipos no canónicos" in rejected.stderr
                    )


if __name__ == "__main__":
    unittest.main()
