# KardioSense — Research Code

[![CI](https://github.com/crisomara/kardiosense-research/actions/workflows/ci.yml/badge.svg)](https://github.com/crisomara/kardiosense-research/actions/workflows/ci.yml)
[![Security](https://github.com/crisomara/kardiosense-research/actions/workflows/security.yml/badge.svg)](https://github.com/crisomara/kardiosense-research/actions/workflows/security.yml)

Open-source research code for lead-agnostic ECG + clinical-risk-factor fusion, targeting myocardial infarction (MI) screening in low-resource settings.

This repository contains the model architecture, training/evaluation harnesses, data-preprocessing code, and the ISIBrno-AIMT benchmark comparison pipeline referenced in the accompanying manuscript. See `MODEL_CARD.md` for intended use, training data provenance, and known limitations before using or citing any result here.

**Before trying to reproduce a result:** read `REPRODUCING.md` (data access, run order, and what isn't pinned/guaranteed) and `BENCHMARK_PIPELINE.md` (why the six benchmark notebooks are separate, and in what order they depend on each other). See `REFERENCES.md` for citations for every dataset, the ISIBrno-AIMT comparison baseline, and the key software this code depends on.

## What's in `notebooks/`

| Notebook | Purpose |
|---|---|
| `01_ecg_baseline` | Single-lead PTB-XL baseline ResNet-1D |
| `02_ecg_lead_agnostic` | Lead-masked training, 1- to 6-lead graceful degradation |
| `02b_ecg_external_code15` | External validation on CODE-15% (Brazil) |
| `02d_fusion_external_mimic` | MIMIC-IV external validation attempt (currently blocked — see Model Card) |
| `03_clinical_nhanes` | XGBoost clinical risk-factor branch (NHANES) |
| `04_fusion_architecture` | Cross-attention ECG+clinical fusion (synthetic training data — see Model Card) |
| `05_export_tflite` | On-device TFLite export |
| `06`–`11` | ISIBrno-AIMT head-to-head benchmark, Steps 1–5 (normalised eval, threshold sharing, lead ablation, cross-lead attention, 12-lead, CODE-15% cross-country) |

## What's deliberately not here

- **Trained weights.** Available on request under a signed research-use, non-commercial license — see `MODEL_CARD.md`.
- **The African field ECG pilot notebook and data.** Withheld pending institutional ethics/consent approval.
- **Production app / backend / business logic.** Kept in a separate, private repository.

## Configuration

Notebooks default to `BASE_DIR = '/content/drive/MyDrive/KardioSenseAI'` for Colab+Drive use, overridable via the `KARDIOSENSE_BASE_DIR` environment variable. The MIMIC-IV notebook reads its BigQuery project from `KARDIOSENSE_GCP_PROJECT` (defaults to a placeholder — set this to your own PhysioNet-credentialed project).

## Running with Docker

See `DOCKER.md` for two pinned-environment images (core pipeline + a separate TFLite-export image) — this replaces "whatever Colab happens to have today" with an explicit, version-pinned environment. Read it before assuming a container run reproduces a result; it's honest about what pinning does and doesn't solve for Colab-authored notebooks.

## CI

GitHub Actions runs on every push and pull request. No notebook is executed in CI (they need PhysioNet, Drive or BigQuery data and GPU training).

- **CI** (`ci.yml`): ruff over the helper scripts, tests and notebooks (notebooks are held to correctness rules only: syntax errors and undefined names, see `ruff.toml`); `scripts/check_notebooks.py` validates every notebook against the nbformat schema, enforces a 5 MB per-notebook size budget and writes sizes and output counts to the job summary; pytest with coverage.
- **Docker build** (`docker.yml`): builds both pinned images without pushing, only when a Dockerfile, `requirements.txt` or a notebook changes.
- **Security** (`security.yml`, also weekly): gitleaks over the full history, pip-audit on the pinned requirements, CodeQL (Python), dependency review on pull requests, and actionlint on the workflows.
- Dependabot opens grouped weekly updates for pip, Docker base images and GitHub Actions.

Run the same checks locally:

```bash
pip install -r requirements-ci.txt
ruff check . && ruff format --check scripts tests
python scripts/check_notebooks.py
pytest -q
```

## Secret scanning

`.gitleaks.toml` + `.pre-commit-config.yaml` configure [gitleaks](https://github.com/gitleaks/gitleaks) for anyone using the `pre-commit` framework. A dependency-free fallback also runs without any extra install: `git config core.hooksPath .githooks` enables `.githooks/pre-commit`, which blocks commits containing AWS keys, private-key blocks, hardcoded credential assignments, or real-looking email addresses.

## License

Code: Apache License 2.0 (see `LICENSE`) — chosen over MIT specifically for its explicit patent grant.

Model weights, when released, are under a separate research-use license — not Apache 2.0. See `MODEL_CARD.md`.

## Citation

See `CITATION.cff`.
