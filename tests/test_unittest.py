from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_code_auditor.pipeline import run_audit
from agent_code_auditor.reporter import render_markdown


class AgentCodeAuditorTests(unittest.TestCase):
    def test_demo_audit_finds_expected_risks(self) -> None:
        state = run_audit(Path("demo/sample_project"))
        titles = {finding.title for finding in state.findings}

        self.assertEqual(len(state.scanned_files), 2)
        self.assertIn("Possible secret committed to source", titles)
        self.assertIn("Dynamic code execution", titles)
        self.assertIn("Broad exception handling", titles)
        self.assertIn("Unfinished implementation marker", titles)

    def test_report_contains_workflow_and_verification(self) -> None:
        state = run_audit(Path("demo/sample_project"))
        report = render_markdown(state)

        self.assertIn("Agent Workflow", report)
        self.assertIn("Verification", report)
        self.assertIn("Verifier check passed", report)
        self.assertIn("sample_project", report)


if __name__ == "__main__":
    unittest.main()
