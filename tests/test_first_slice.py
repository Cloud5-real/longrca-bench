from __future__ import annotations

import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER_URL = "https://arxiv.org/abs/2608.15242"
DATASET_URL = "https://huggingface.co/datasets/CLoud5-real/longrca-bench"
GITHUB_URL = "https://github.com/Cloud5-real/longrca-bench"


class FirstSliceTest(unittest.TestCase):
    def test_hero_stats_and_leaderboard_surface_exist(self) -> None:
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(
            "Long-Horizon Root-Cause Localization.",
            html,
        )
        self.assertIn(
            "1,140 trajectories · 5 benchmarks · exact step localization.", html
        )
        self.assertNotIn("Diagnosing <em>who</em>", html)
        self.assertNotIn(">Who?<", html)
        self.assertNotIn(">When?<", html)
        for url in (PAPER_URL, DATASET_URL, GITHUB_URL):
            self.assertIn(url, html)
        for anchor in ("overview", "leaderboard"):
            self.assertIn(f'id="{anchor}"', html)
        self.assertIn('id="benchmark-stats"', html)
        self.assertIn('id="leaderboard-body"', html)
        self.assertIn('href="assets/styles.css"', html)
        self.assertIn('src="assets/app.js"', html)

    def test_hero_resource_links_have_local_icons(self) -> None:
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        for icon in ("arxiv.svg", "huggingface.svg", "github.svg"):
            relative_path = f"assets/icons/{icon}"
            self.assertIn(f'src="{relative_path}"', html)
            self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_resource_icons_preserve_brand_colors(self) -> None:
        expected_colors = {
            "arxiv.svg": "#B31B1B",
            "huggingface.svg": "#FFD21E",
            "github.svg": "#181717",
        }
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        for icon, expected_color in expected_colors.items():
            with self.subTest(icon=icon):
                root = ET.parse(REPO_ROOT / "assets" / "icons" / icon).getroot()
                paths = root.findall(".//svg:path", namespace)
                self.assertTrue(paths)
                self.assertEqual(
                    {expected_color},
                    {path.get("fill") for path in paths},
                )

    def test_leaderboard_is_model_first_and_step_exact_focused(self) -> None:
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        headers = [
            "Model",
            "Method",
            "Overall",
            "SWE-bench Pro",
            "Terminal-Bench 2",
            "TravelPlanner",
            "VitaBench",
            "WebArena",
        ]
        positions = [html.index(f">{header}<") for header in headers]
        self.assertEqual(sorted(positions), positions)
        table_head = html[html.index("<thead>") : html.index("</thead>")]
        self.assertNotIn(">Role Acc.<", table_head)
        self.assertNotIn(">Root ±5<", table_head)
        self.assertNotIn(">Root MAE ↓<", table_head)

    def test_site_metadata_contains_approved_statistics(self) -> None:
        site = json.loads((REPO_ROOT / "data" / "site.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [
                ("Trajectories", "1,140"),
                ("Benchmarks", "5"),
                ("Median steps", "145"),
                ("Median root-to-end", "48"),
            ],
            [(stat["label"], stat["value"]) for stat in site["stats"]],
        )

    def test_javascript_fetches_the_unique_leaderboard_source(self) -> None:
        script = (REPO_ROOT / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn('fetch("data/leaderboard.json")', script)
        self.assertIn("root_exact_correct", script)
        self.assertIn("benchmark_slices", script)
        self.assertIn("by_benchmark", script)
        for method in ("RCTA", "ECHO", "All-at-once", "Step-by-step"):
            self.assertNotIn(f'"{method}"', script)


if __name__ == "__main__":
    unittest.main()
