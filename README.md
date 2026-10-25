# KardioSense research code

[![CI](https://github.com/crisomara/kardiosense-research/actions/workflows/ci.yml/badge.svg)](https://github.com/crisomara/kardiosense-research/actions/workflows/ci.yml)
[![Security](https://github.com/crisomara/kardiosense-research/actions/workflows/security.yml/badge.svg)](https://github.com/crisomara/kardiosense-research/actions/workflows/security.yml)

Research code for lead-agnostic ECG and clinical risk-factor fusion, aimed at screening for myocardial infarction (MI) in low-resource settings. It is published so that researchers can inspect, run and test the methods, and so that the results reported for KardioSense can be checked.

The repository holds the model architecture, the training and evaluation code and the data preprocessing used in the accompanying manuscript. Read `MODEL_CARD.md` for intended use, training data and known limitations before using or citing any result here.

## Research use only

- This is research software. It is not a medical device and has not been validated for clinical use.
- Do not use it, or any model trained with it, to diagnose or treat anyone, or to make decisions about a patient's care.
- Trained model weights are not distributed in this repository.

## Licence and permitted use

The code is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE).

- You may use, run, change and share it for research, teaching and personal non-commercial purposes. Universities, public research institutes, charities, health organisations and government bodies may use it for any purpose that licence allows, whatever their source of funding.
- Any commercial use needs written permission from KardioSense first. That includes using the code, or anything built from it, in a product or service, and any use by or for a company.
- To ask for permission, contact KardioSense at [mail.cardiosense@gmail.com](mailto:mail.cardiosense@gmail.com).
- Versions of this repository whose `LICENSE` file is the Apache License 2.0, including every version published before 25 October 2026, remain under that licence for anyone who received them. Versions whose `LICENSE` file is the PolyForm Noncommercial License 1.0.0 are under that licence.

## Before you reproduce a result

- `REPRODUCING.md`: data access, run order, and what is not pinned or guaranteed.
- `REFERENCES.md`: citations for every dataset and the key software used.

## What is in `notebooks/`

| Notebook | Purpose |
|---|---|
| `01_ecg_baseline` | Single-lead PTB-XL baseline ResNet-1D |
| `02_ecg_lead_agnostic` | Lead-masked training, 1- to 6-lead graceful degradation |
| `02b_ecg_external_code15` | External validation on CODE-15% (Brazil) |
| `02d_fusion_external_mimic` | MIMIC-IV external validation attempt (currently blocked, see the model card) |
| `03_clinical_nhanes` | XGBoost clinical risk-factor branch (NHANES) |
| `04_fusion_architecture` | Cross-attention ECG and clinical fusion (synthetic training data, see the model card) |
| `05_export_tflite` | On-device TFLite export |

## What is deliberately not here

- **Trained weights.** Available on request under a signed research-use, non-commercial licence. See `MODEL_CARD.md`.
- **Patient-level data.** No dataset, record or per-patient row is stored here. Every dataset is downloaded from its original source under that source's own terms (see `REPRODUCING.md`).
- **The African field ECG pilot notebook and data.** Withheld pending institutional ethics and consent approval.
- **The production app, backend and business logic.** Kept in a separate, private repository.

## Configuration

The notebooks default to `BASE_DIR = '/content/drive/MyDrive/KardioSenseAI'` for Colab with Google Drive. Set the `KARDIOSENSE_BASE_DIR` environment variable to use another folder. The MIMIC-IV notebook reads its BigQuery project from `KARDIOSENSE_GCP_PROJECT`; set it to your own PhysioNet-credentialed project.

## Running with Docker

`DOCKER.md` describes two pinned images: the core pipeline (`Dockerfile`, packages from `requirements.txt`) and a separate TFLite export image (`Dockerfile.tflite_export`, packages from `requirements-export.txt`). They replace "whatever Colab has today" with an explicit, version-pinned environment. Read `DOCKER.md` before assuming a container run reproduces a result: it explains what pinning does and does not solve for notebooks written in Colab.

## Continuous integration

GitHub Actions runs on every push and pull request. No notebook is executed in CI, because they need PhysioNet, Drive or BigQuery data and GPU training.

- **CI** (`ci.yml`): Ruff lint and format checks over the whole repository, including the notebooks (rules in `ruff.toml`); `scripts/check_notebooks.py`, which validates every notebook against the nbformat schema, enforces a 5 MB size budget per notebook and writes sizes and output counts to the job summary; pytest with coverage.
- **Docker build** (`docker.yml`): builds both pinned images without pushing, only when a Dockerfile, a requirements file or a notebook changes.
- **Security** (`security.yml`, also weekly): gitleaks over the full history, pip-audit on the pinned requirements (advisory only for the offline export toolchain), CodeQL for Python, dependency review on pull requests, and actionlint on the workflows.
- Dependabot opens grouped weekly updates for pip, Docker base images and GitHub Actions.

Run the same checks locally:

```bash
pip install -r requirements-ci.txt
ruff check . && ruff format --check .
python scripts/check_notebooks.py
python -m pytest -q
```

## Contributing and secret scanning

`CONTRIBUTING.md` sets out the code standard and what may never be committed (weights, data, per-record rows, secrets). `.pre-commit-config.yaml` runs the same Ruff rules and formatting, basic file checks and [gitleaks](https://github.com/gitleaks/gitleaks) before each commit: `pip install pre-commit`, then `pre-commit install`. A fallback with no extra install is also available: `git config core.hooksPath .githooks` enables `.githooks/pre-commit`, which blocks commits containing AWS keys, private-key blocks, hardcoded credential assignments or real-looking email addresses.

## Citation

See `CITATION.cff`.
