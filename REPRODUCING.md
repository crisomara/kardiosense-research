# Reproducing These Results

## What you need before starting

| Data source | Access | Notes |
|---|---|---|
| PTB-XL | Open, no account | Downloaded directly by `01_ecg_baseline.ipynb` |
| NHANES | Open, no account | Downloaded directly by `03_clinical_nhanes.ipynb` |
| CODE-15% | Open (Zenodo) **or** credentialed (PhysioNet) | `02b_ecg_external_code15.ipynb` uses the open Zenodo mirror (record 4916206); no account is needed. |
| MIMIC-IV-ECG | Credentialed (PhysioNet + CITI training) | `02d_fusion_external_mimic.ipynb`. As of this writing, our own credentialing has a table-level permission gap (`mimiciv_hosp.admissions`); see `MODEL_CARD.md`. |

No trained model weights are included in this repository (see `MODEL_CARD.md`). To reproduce the reported numbers you need to retrain from scratch by running the notebooks in the order below.

## Run order

**Stage 1: build the checkpoints.**
1. `01_ecg_baseline.ipynb`: single-lead baseline, builds the PTB-XL preprocessed cache everything else reuses
2. `02_ecg_lead_agnostic.ipynb`: produces `checkpoints/kardiosense_ecg_best_mi.pt` (the main ECG checkpoint nearly every later notebook loads)
3. `03_clinical_nhanes.ipynb`: produces the NHANES-tuned clinical (XGBoost) checkpoint
4. `04_fusion_architecture.ipynb`: produces the fusion checkpoint (trained on **synthetically paired** ECG and clinical data, see `MODEL_CARD.md`)
5. `05_export_tflite.ipynb`: on-device export, depends on notebook 2's checkpoint

**Stage 2: external validation.**
- `02b_ecg_external_code15.ipynb` and `02d_fusion_external_mimic.ipynb` both load the Stage 1 checkpoints and require no further training.

## Reproducibility caveats

- **Pinned versions only in the Docker images.** In Colab every notebook installs its packages with `!pip install` and no version pins. `requirements.txt` and `requirements-export.txt` pin the versions used by the two Docker images (see `DOCKER.md`); they were chosen after the original runs, so they are a reproducible environment, not a record of the exact versions behind each reported number.
- **Fixed seeds (`SEED = 42`) do not guarantee bit-identical results** across different hardware, CUDA versions, or library versions. Expect numbers close to those reported, not necessarily identical to the last decimal place.
- **Stochastic training**: several notebooks retrain models rather than loading fixed weights; small AUC differences between runs are expected and do not by themselves indicate a bug.
