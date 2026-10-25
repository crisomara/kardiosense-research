# ISIBrno-AIMT Benchmark Pipeline (notebooks 06-11)

These six notebooks are not six independent copies of the same experiment — they're
a linear pipeline, each stage consuming artifacts the previous stage produced and
answering a distinct question that maps to a specific part of the manuscript. That's
why they're kept as separate notebooks rather than merged into one: TRIPOD+AI-style
reporting benefits from being able to point to a single, independently re-runnable
notebook per claim, and a class-level diff (see below) confirms the model
definitions genuinely differ between steps rather than being copy-pasted filler.

| Step | Notebook | Question it answers | Consumes | Produces |
|---|---|---|---|---|
| 1 | `06_benchmark_step1_isibrno_normalised` | Are both models being judged on identical records/labels? | PTB-XL cache (NB01/02), fold-10 split | `preds_isibrno_fold10.npy`, `labels_test_fold10.npy` |
| 2 | `07_benchmark_step2_isibrno_threshold` | Shared evaluation harness / threshold handling | Step 1 outputs + NB02 checkpoint | Shared eval results |
| 3 | `08_benchmark_step3_isibrno_leadablation` | How does each model degrade as leads are removed (1L-6L)? | Step 2 outputs | Lead-ablation table (the numbers cited in the manuscript's Table 3) |
| 4A | `09_benchmark_step4a_crosslead_attention` | Does adding cross-lead attention close the remaining NORM/STTC gap at 6-lead? | Step 3 findings | Cross-lead attention ablation results |
| 4B | `10_benchmark_step4b_12lead` | Can KardioSense compete with ISIBrno natively at 12-lead? | Step 3 findings, retrains at `n_leads=12` | 12-lead comparison results |
| 5 | `11_benchmark_step5_code15_crosscountry` | Do the PTB-XL findings (Steps 1-4) hold on an independent country/hardware/population (Brazil)? | Steps 3 & 4B results, CODE-15% data | External cross-country validation table |

## Why not merge them

A quick check of the model class definitions (`ResBlock1D`, `AttentionPool`,
`KardioSenseECGModel`, `ISIBrnoResidualBlock`, `ISIBrnoNN`) that appear in more than
one of these notebooks found **3-4 distinct variants of each**, not one copy-pasted
version — each notebook tests a different lead count, attention mechanism, or
training configuration on purpose. Extracting these into one shared module would
risk silently conflating configurations that are supposed to differ between
benchmark steps. If you want a shared-utilities refactor anyway (e.g. to cut
boilerplate like Drive mounting / package installs), that's safe to do, but each
notebook would need to be re-run afterward to confirm nothing broke — that needs
an actual Colab session, which wasn't available for this pass.

## What was actually streamlined in this pass

- Consistent `NN_phase_description.ipynb` naming (see main folder) so the step
  order is visible at a glance in a file listing, instead of the previous mixed
  `KardioSense_0N_...` / `KardioSense_0Na_...` scheme.
- Notebook 11 had seven leftover ad hoc diagnostic/debug cells appended after its
  own "Complete" marker (from the CODE-15% bug-hunting session) — removed, since
  their findings are now properly integrated into the notebook's Sections 2/3/6.
