# References

Every dataset, comparison baseline, and challenge referenced by this codebase. Software library citations are included for completeness; dataset and baseline citations are the ones that matter for reproducing or citing a result.

## Datasets

**PTB-XL** (notebooks 01, 02, and as the training/internal-test set for 06-11)
- Wagner, P., Strodthoff, N., Bousseljot, R.-D., Kreiseler, D., Lunze, F. I., Samek, W., & Schaeffter, T. (2020). PTB-XL: A large publicly available ECG dataset. *Scientific Data*, 7, 154. https://doi.org/10.1038/s41597-020-0495-6
- Wagner, P., Strodthoff, N., Bousseljot, R., Samek, W., & Schaeffter, T. (2020). PTB-XL, a large publicly available electrocardiography dataset (version 1.0.3). PhysioNet. https://doi.org/10.13026/qgmg-0d46

**CODE-15%** (notebook 02b, and as the cross-country external validation set in 11)
- Ribeiro, A. H., Paixão, G. M. M., Lima, E. M., Ribeiro, M. H., Pinto Filho, M. M., Gomes, P. R., Oliveira, D. M., & Meira Jr., W. CODE-15%: a large scale annotated dataset of 12-lead ECGs. Zenodo. https://doi.org/10.5281/zenodo.4916206
- Companion model paper: Ribeiro, A. H., Ribeiro, M. H., Paixão, G. M. M., et al. (2020). Automatic diagnosis of the 12-lead ECG using a deep neural network. *Nature Communications*, 11, 1760. https://doi.org/10.1038/s41467-020-15432-4

**NHANES** (notebook 03, clinical risk-factor branch)
- Centers for Disease Control and Prevention (CDC), National Center for Health Statistics (NCHS). National Health and Nutrition Examination Survey Data. Hyattsville, MD: U.S. Department of Health and Human Services, CDC.

**MIMIC-IV-ECG** (notebook 02d, external validation attempt — see `MODEL_CARD.md` for its current access-blocked status)
- Gow, B., Pollard, T., Nathanson, L. A., Johnson, A., Moody, B., Fernandes, C., Greenbaum, N., Waks, J. W., Eslami, P., Carbonati, T., Chaudhari, A., Herbst, E., Moukheiber, D., Berkowitz, S., Mark, R., & Horng, S. (2023). MIMIC-IV-ECG: Diagnostic Electrocardiogram Matched Subset (version 1.0). PhysioNet. https://doi.org/10.13026/4nqg-sb35

**PhysioNet resource citation** (required alongside the above for PTB-XL and MIMIC-IV, both PhysioNet-hosted)
- Goldberger, A. L., Amaral, L. A. N., Glass, L., Hausdorff, J. M., Ivanov, P. Ch., Mark, R. G., Mietus, J. E., Moody, G. B., Peng, C. K., & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. *Circulation*, 101(23), e215-e220. https://doi.org/10.1161/01.CIR.101.23.e215

## Benchmark comparison baseline

**ISIBrno-AIMT** (notebooks 06-11 — the model these benchmarks compare KardioSense against; architecture ported from their own `model_code.py`)
- Nejedly, P., Ivora, A., Smisek, R., Viscor, I., Koscova, Z., Jurak, P., & Plesinger, F. (2021). Classification of ECG using ensemble of residual CNNs with attention mechanism. *2021 Computing in Cardiology (CinC)*, Brno, Czech Republic. IEEE. https://doi.org/10.23919/CinC53138.2021.9662723

**PhysioNet/Computing in Cardiology Challenge 2021** (the challenge ISIBrno-AIMT won and this benchmark is framed against)
- Reyna, M. A., Sadr, N., Perez Alday, E. A., Gu, A., Shah, A. J., Robichaux, C., Rad, A. B., Elola, A., Seyedi, S., Ansari, S., Ghanbari, H., Li, Q., Sharma, A., & Clifford, G. D. (2021). Will two do? Varying dimensions in electrocardiography: The PhysioNet/Computing in Cardiology Challenge 2021. *Computing in Cardiology 2021*, 48, 1-4. https://doi.org/10.23919/CinC53138.2021.9662687

## Software

- Paszke, A., et al. (2019). PyTorch: An imperative style, high-performance deep learning library. *NeurIPS 2019*.
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD '16*. https://doi.org/10.1145/2939672.2939785
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *NeurIPS 2017*.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.
- Makowski, D., Pham, T., Lau, Z. J., Brammer, J. C., Lespinasse, F., Pham, H., Schölzel, C., & Chen, S. A. (2021). NeuroKit2: A Python toolbox for neurophysiological signal processing. *Behavior Research Methods*, 53(4), 1689-1696. https://doi.org/10.3758/s13428-020-01516-y
- WFDB software package — cite via the PhysioNet resource citation above (Goldberger et al., 2000).
