# Model Card — KardioSense ECG + Clinical Fusion

Following the reporting structure recommended by MI-CLAIM (Minimum Information About Clinical AI Modeling).

## Intended use

- **Primary use case:** Screening-level myocardial infarction (MI) detection from reduced-lead ECG (down to single-lead) in low-resource settings where full 12-lead acquisition or specialist interpretation is not readily available.
- **Not intended for:** Standalone diagnosis, replacing a clinician's ECG interpretation, or use on populations outside the age/demographic ranges represented in the training and validation data described below.
- **Output:** Per-class probability for NORM, MI, AFIB, STTC, CD from ECG; a separate 10-year CVD risk estimate from clinical risk factors; a fused risk score combining both when clinical data is available.

## Model architecture (public — see `notebooks/`)

- **ECG branch:** ResNet-1D stem + residual blocks → BiLSTM (×2) → multi-head self-attention → attention pooling → lead-mask-conditioned classifier head. Trained with random lead masking so the same weights degrade gracefully from 12-lead down to 1-lead input.
- **Clinical branch:** XGBoost gradient-boosted trees over standard cardiovascular risk factors (age, sex, BP, BMI, smoking, lipids, HbA1c where available).
- **Fusion:** Cross-attention gate combining the 256-dim ECG embedding with the clinical branch's output.

Full architecture code, training harness, and the ISIBrno-AIMT benchmark comparison pipeline are in `notebooks/`. Only the trained weights are withheld (see "What is not in this repository" below).

## Training data provenance

| Dataset | Role | Population |
|---|---|---|
| PTB-XL | ECG model training + internal test | Germany, Schiller AG hardware, cardiologist-labeled |
| CODE-15% | External validation | Brazil, Tecnomed/Nihon Kohden hardware, algorithm-assisted labels |
| MIMIC-IV-ECG | External validation (blocked — see limitations) | USA, GE/Philips hardware, ICD-10 + cardiologist labels |
| NHANES | Clinical risk-factor branch training | USA, cross-sectional survey |
| Fusion training data | Fusion gate training | **Synthetic** — see limitation below |

MI prevalence and AUC targets, per-notebook, are documented in each notebook's own markdown cells.

## Known failure modes and limitations

- **AFib internal/external discrepancy:** A small internal test sample (2–15 AFib cases) produces a saturated AUC (1.000) for both KardioSense and the ISIBrno-AIMT baseline alike — this is a small-sample artefact, not evidence of leakage, but it means the internal AFib number should not be read as a stable estimate. The external (CODE-15%) AFib AUC is the more reliable estimate of real-world performance.
- **STTC external validation:** Fails its target AUC on CODE-15% external validation. This is reported, not hidden.
- **ISIBrno-AIMT comparison training asymmetry:** The head-to-head benchmark (`notebooks/06`–`11`) uses augmentation strategies that differ between the two models in ways documented in each notebook; at native 12-lead input, ISIBrno-AIMT outperforms KardioSense. A masking-matched re-run is a recommended future step, not yet done.
- **Fusion model trained on synthetic data:** The ECG+clinical fusion gate (`notebooks/04_fusion_architecture.ipynb`) is trained on synthetically paired ECG/clinical records, printed explicitly in that notebook's own output. It has not yet been validated on genuinely paired real-world ECG+clinical data — see MIMIC-IV status below.
- **MIMIC-IV external validation blocked:** `notebooks/02d_fusion_external_mimic.ipynb` documents an access-denied error (table-level BigQuery permission gap) rather than a completed validation. No claims in this repository or an associated manuscript should describe MIMIC-IV validation as complete.
- **CODE-15% cross-country notebook (`notebooks/11`):** Recently had three data-pipeline bugs fixed (HDF5/exam_id index misalignment, an incorrect signal-scale assumption, and an incorrect label-remapping step) — see the inline comments in that notebook referencing the fix. The fix has been merged and reviewed against the notebook's own captured diagnostic output, but has not yet been re-run end-to-end against live data; treat its results as provisional until a full re-run is recorded.
- **No confidence intervals yet:** AUCs throughout the notebook set are point estimates. Bootstrap confidence intervals are a planned addition, not yet implemented.

## What is not in this repository

- Trained model weights (`.pt` / `.pkl` checkpoints) — available on request under a signed research-use, non-commercial license.
- Production mobile app, backend API, and deployment/business logic.
- The African field ECG pilot notebook and any of its data or outputs — withheld pending institutional ethics/consent approval, independent of the open-source licensing question.
- Pricing, business model, or investor material.

## Reporting standards

This work is being prepared for reporting under TRIPOD+AI and PROBAST+AI. The architecture and evaluation code in this repository is published specifically to satisfy the full-transparency expectations of those standards.
