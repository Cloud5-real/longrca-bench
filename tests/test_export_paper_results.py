from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import export_paper_results as exporter  # noqa: E402


SOURCE_RECORDS = (
    REPO_ROOT.parent
    / "agent-bench"
    / "baseline_results"
    / "rcta_clean_prompt_deepseek_v4_flash_20260731"
    / "final_evaluation_results"
    / "records.tsv"
)


class ExportPaperResultsTest(unittest.TestCase):
    def test_normalize_role_only_removes_explicit_handoff_suffix(self) -> None:
        self.assertEqual(
            "diagnostagent",
            exporter.normalize_role("  DiagnostAgent (-> ActionAgent)  "),
        )
        self.assertEqual(
            "diagnostagent",
            exporter.normalize_role("DiagnostAgent (→ JudgeAgent)"),
        )
        self.assertEqual("planner (review)", exporter.normalize_role("Planner (Review)"))

    def test_explicit_predicted_agent_is_scored_independently(self) -> None:
        fields = [
            "method",
            "method_label",
            "qid",
            "predicted_agent",
            "predicted_role_derived",
            "ground_truth_agent",
            "step_exact",
            "step_within_5",
            "step_abs_err",
            "step_valid",
            "failed",
        ]
        row = {
            "method": "agent_error_trajectory_analysis",
            "method_label": "RCTA",
            "qid": "sample-1",
            "predicted_agent": "CorrectRole",
            "predicted_role_derived": "WrongRole",
            "ground_truth_agent": "CorrectRole",
            "step_exact": "True",
            "step_within_5": "True",
            "step_abs_err": "0",
            "step_valid": "True",
            "failed": "False",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records.tsv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
                writer.writeheader()
                writer.writerow(row)

            result = exporter.build_leaderboard(path, expected_n=None)

        self.assertEqual(1, result["results"][0]["role_correct"])

    @unittest.skipUnless(
        SOURCE_RECORDS.is_file(),
        "canonical source records are available only in the local research workspace",
    )
    def test_canonical_records_reproduce_paper_table(self) -> None:
        payload = exporter.build_leaderboard(SOURCE_RECORDS)
        results = payload["results"]

        self.assertEqual(
            [
                "RCTA",
                "ECHO",
                "All-at-once",
                "Step-by-step",
                "Binary search",
                "FALAT",
            ],
            [row["method"] for row in results],
        )
        expected = {
            "RCTA": (583, 275, 426, 38.6),
            "ECHO": (314, 150, 282, 50.4),
            "All-at-once": (299, 87, 227, 55.9),
            "Step-by-step": (253, 60, 193, 52.3),
            "Binary search": (262, 39, 152, 61.7),
            "FALAT": (217, 32, 142, 66.6),
        }
        for row in results:
            role, exact, within_five, mae = expected[row["method"]]
            with self.subTest(method=row["method"]):
                self.assertEqual(1140, row["n"])
                self.assertEqual(role, row["role_correct"])
                self.assertEqual(exact, row["root_exact_correct"])
                self.assertEqual(within_five, row["root_within_5_correct"])
                self.assertEqual(mae, round(row["root_mae"], 1))
                self.assertEqual("DeepSeek-V4-Flash", row["model"])
                self.assertEqual("Paper Result", row["status"])


if __name__ == "__main__":
    unittest.main()
