from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER_URL = "https://arxiv.org/abs/2608.15242"
DATASET_URL = "https://huggingface.co/datasets/CLoud5-real/longrca-bench"
GITHUB_URL = "https://github.com/Cloudreal/longrca-bench"


class FirstSliceTest(unittest.TestCase):
    def test_hero_stats_and_leaderboard_surface_exist(self) -> None:
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(
            "LongRCA Bench: Diagnosing Responsible Roles and Root Causes in "
            "Long-Horizon Agent Failures",
            html,
        )
        for url in (PAPER_URL, DATASET_URL, GITHUB_URL):
            self.assertIn(url, html)
        for anchor in ("overview", "leaderboard"):
            self.assertIn(f'id="{anchor}"', html)
        self.assertIn('id="benchmark-stats"', html)
        self.assertIn('id="leaderboard-body"', html)
        self.assertIn('href="assets/styles.css"', html)
        self.assertIn('src="assets/app.js"', html)

    def test_site_metadata_contains_approved_statistics(self) -> None:
        site = json.loads((REPO_ROOT / "data" / "site.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [
                ("Trajectories", "1,140"),
                ("Domains", "5"),
                ("Median steps", "145"),
                ("Median root-to-end", "48"),
            ],
            [(stat["label"], stat["value"]) for stat in site["stats"]],
        )

    def test_javascript_fetches_the_unique_leaderboard_source(self) -> None:
        script = (REPO_ROOT / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn('fetch("data/leaderboard.json")', script)
        self.assertIn("root_exact_correct", script)
        self.assertIn("role_correct", script)
        self.assertIn("root_within_5_correct", script)
        for method in ("RCTA", "ECHO", "All-at-once", "Step-by-step"):
            self.assertNotIn(f'"{method}"', script)


if __name__ == "__main__":
    unittest.main()
