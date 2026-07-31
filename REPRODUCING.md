# Reproducing These Results

## What you need before starting

| Data source | Access | Notes |
|---|---|---|
| PTB-XL | Open, no account | Downloaded directly by `01_ecg_baseline.ipynb` |
| NHANES | Open, no account | Downloaded directly by `03_clinical_nhanes.ipynb` |
| CODE-15% | Open (Zenodo) **or** credentialed (PhysioNet) | `02b_ecg_external_code15.ipynb` uses the open Zenodo mirror (record 4916206) — no account needed. `11_benchmark_step5_code15_crosscountry.ipynb` uses the PhysioNet mirror instead, which does require a free PhysioNet account. Same dataset, two access paths — use whichever notebook you're running. |
| MIMIC-IV-ECG | Credentialed (PhysioNet + CITI training) | `02d_fusion_external_mimic.ipynb` — as of this writing, our own credentialing has a table-level permission gap (`mimiciv_hosp.admissions`); see `MODEL_CARD.md`. |

No trained model weights are included in this repository (see `MODEL_CARD.md`). To reproduce the reported numbers you need to retrain from scratch by running the notebooks in the order below.

## Run order

**Stage 1 — build the checkpoints:**
1. `01_ecg_baseline.ipynb` — single-lead baseline, builds the PTB-XL preprocessed cache everything else reuses
2. `02_ecg_lead_agnostic.ipynb` — produces `checkpoints/kardiosense_ecg_best_mi.pt` (the main ECG checkpoint nearly every later notebook loads)
3. `03_clinical_nhanes.ipynb` — produces the NHANES-tuned clinical (XGBoost) checkpoint
4. `04_fusion_architecture.ipynb` — produces the fusion checkpoint (trained on **synthetically paired** ECG+clinical data — see `MODEL_CARD.md`)
5. `05_export_tflite.ipynb` — on-device export, depends on notebook 2's checkpoint

**Stage 2 — external validation:**
- `02b_ecg_external_code15.ipynb` and `02d_fusion_external_mimic.ipynb` both load the Stage 1 checkpoints and require no further training.

**Stage 3 — ISIBrno-AIMT benchmark (see `BENCHMARK_PIPELINE.md` for the full rationale):**
6. `06_benchmark_step1_isibrno_normalised.ipynb` — trains the ISIBrno-AIMT baseline **from scratch** on your own PTB-XL folds (no external weights needed; architecture ported from the ISIBrno-AIMT team's own `model_code.py`, their PhysioNet/CinC 2021 Challenge entry)
7. `07_benchmark_step2_isibrno_threshold.ipynb` → 8 → 9/10 → 11, each consuming the previous step's saved `.npy`/`.json` results, in that numeric order.

## Reproducibility caveats

- **No pinned dependency versions.** Every notebook installs packages with `!pip install` and no version pins (there is no `requirements.txt` capturing exact versions from the original runs). Expect library drift over time; if you need an exact match, pin `torch`, `xgboost`, `scipy`, and `wfdb` to recent-as-of-2026 versions and note what you used.
- **Fixed seeds (`SEED = 42`) do not guarantee bit-identical results** across different hardware, CUDA versions, or library versions — expect numbers close to those reported, not necessarily identical to the last decimal place.
- **Stochastic training**: several notebooks retrain models (KardioSense variants, ISIBrno-AIMT) rather than loading fixed weights; small AUC differences between runs are expected and do not by themselves indicate a bug.
