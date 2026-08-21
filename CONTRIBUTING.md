# Contributing results

LongRCA Bench accepts community results through a reviewed GitHub pull request. A submission appears on the leaderboard only after automated validation and maintainer review succeed and the pull request is merged.

The evaluation labels are public. Please present submissions as reproducibility results, not as performance on a hidden test set.

## Submission layout

Create one directory under `submissions/<submission-id>/` containing these files:

```text
submissions/<submission-id>/
├── metadata.json
├── predictions.jsonl
└── REPRODUCE.md
```

### `metadata.json`

Include at least:

```json
{
  "submission_id": "team-method-model-yyyymmdd",
  "method": "Method name",
  "model": "Model name and version",
  "provider": "Model provider or organization",
  "authors": ["Contributor name"],
  "date": "YYYY-MM-DD",
  "code_url": "https://github.com/example/repository",
  "logs_url": "https://example.org/public-run-artifacts",
  "license": "License for the submitted prediction artifact"
}
```

Use absolute public HTTPS URLs. Do not include credentials, private endpoints, or expiring signed URLs.

### `predictions.jsonl`

Submit exactly **1,140** JSON Lines records, one for every public trajectory. Each `question_ID` must occur exactly once.

```json
{"question_ID":"<dataset id>","predicted_role":"<responsible role>","predicted_step":42}
```

- `question_ID`: exact ID from the released dataset.
- `predicted_role`: the method's explicit responsible-role prediction. It is scored independently and must not be inferred from the actor at `predicted_step`.
- `predicted_step`: zero-based integer index into the released trajectory history.

Do not add gold labels, copied annotations, full trajectories, prompts, or logs to this file.

### `REPRODUCE.md`

Document the environment, model endpoint or weights, prompt/template version, decoding settings, random seeds, commands, hardware or service configuration, and expected runtime/cost. A maintainer should be able to understand how the submitted file was produced.

## Large logs and traces

Keep raw traces, logs, and other large artifacts in durable external storage. Put a public link in `metadata.json`; do not commit large logs directly to the Pages repository.

## Pull request review

The pull request checks will verify:

1. JSON syntax and schema.
2. Exactly 1,140 unique dataset IDs and valid field types.
3. Explicit role scoring through `predicted_role`, independent of `predicted_step`.
4. Metric counts, ordering, dates, links, and duplicate submission IDs.
5. Absence of secrets, gold annotation content, and repository-local machine paths.

A maintainer may request clarification or a reproduction run before approval. Once approved, maintainers add an aggregate row to `data/leaderboard.json`; the Pages deployment updates after merge.
