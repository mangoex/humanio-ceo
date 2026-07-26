from __future__ import annotations

import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
