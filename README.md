# KardioSense — Research Code

Open-source research code for lead-agnostic ECG + clinical-risk-factor fusion, targeting myocardial infarction (MI) screening in low-resource settings.

This repository contains the model architecture, training/evaluation harnesses, data-preprocessing code, and the ISIBrno-AIMT benchmark comparison pipeline referenced in the accompanying manuscript. See `MODEL_CARD.md` for intended use, training data provenance, and known limitations before using or citing any result here.

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

## License

Code: Apache License 2.0 (see `LICENSE`) — chosen over MIT specifically for its explicit patent grant.

Model weights, when released, are under a separate research-use license — not Apache 2.0. See `MODEL_CARD.md`.

## Citation

See `CITATION.cff`.
