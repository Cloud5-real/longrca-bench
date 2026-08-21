# LongRCA Bench Leaderboard

The official static leaderboard for **LongRCA Bench: Diagnosing Responsible Roles and Root Causes in Long-Horizon Agent Failures**.

- [Leaderboard](https://cloud5-real.github.io/longrca-bench/)
- [Paper](https://arxiv.org/abs/2608.15242)
- [Dataset](https://huggingface.co/datasets/CLoud5-real/longrca-bench)
- [GitHub](https://github.com/Cloud5-real/longrca-bench)

The first release presents the six paper results on 1,140 public trajectories across five domains. Because the gold labels are public, this site is a reproducibility leaderboard rather than a hidden-test competition.

## Data model

`data/leaderboard.json` is the only source used to render leaderboard rows. It stores exact counts (`role_correct`, `root_exact_correct`, and `root_within_5_correct`) instead of duplicated percentages. The browser computes every displayed percentage from those counts and `n`.

The paper-result exporter scores responsible-role accuracy from the explicit `predicted_agent` column in the evaluation records. It never derives the role from `history[predicted_step].name`. Paper-reported Root MAE values are pinned in the exporter because failed predictions do not serialize a `step_abs_err` in the records table.

## Local preview

No build step or package installation is required.

```bash
python3 -m http.server 8000
```

Then open `http://127.0.0.1:8000/`.

## Reproduce the paper rows

```bash
python3 scripts/export_paper_results.py \
  --records <path-to-records.tsv>
python3 scripts/validate_data.py
python3 -m unittest discover -s tests -v
node --check assets/app.js
```

## Contributing

Community results are submitted through reviewed pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for the required `metadata.json`, 1,140-line `predictions.jsonl`, and reproduction notes.

## Deployment

Merges to `main` are deployed with the official GitHub Pages Actions workflow. All HTML, CSS, JavaScript, JSON, fonts, and images are served from this repository without CDN dependencies.
