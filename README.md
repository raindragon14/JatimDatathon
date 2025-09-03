# OPData — Socioeconomic Feature Engineering, PCA, and Time-Aware Modeling

This repository contains data preparation, feature engineering, principal component analysis (PCA), and time-aware model development for Indonesian kabupaten/kota (district/city) panel data. The accompanying notebook focuses on building robust, interpretable components from socioeconomic indicators and preparing inputs for downstream prediction tasks (e.g., MSME counts or NPL rates).

Contents:
- Clear objectives and scope
- Data dictionary and sources
- Methodology (preprocessing, interpolation, time split, scaling, PCA)
- Modeling approach and evaluation
- Reproducibility and how to run
- Limitations, ethics, and roadmap

---

## 1) Objectives

Primary objectives:
- Construct stable, low-dimensional factors from correlated socioeconomic indicators using PCA.
- Prepare time-aware, leakage-safe training and test sets for downstream predictive modeling.
- Provide interpretable insights via PCA loadings and correlation analysis.

Typical downstream targets (depending on your workflow):
- MSME dynamics (e.g., `Jumlah Perusahaan Kecil`).
- Financial stability metrics (e.g., NPL) when joined with `Data-NPL_baru.csv`.

This repository emphasizes:
- Rigorous preprocessing that respects time directionality.
- Dimensionality reduction to mitigate multicollinearity and improve model generalization.
- Transparent, reproducible pipelines.

---

## 2) Repository Structure

Recommended layout (actual structure may evolve):

```
OPData/
├─ Notebook/
│  └─ Model_Train_Final.ipynb          # Main analysis notebook
├─ data/
│  ├─ raw/
│  │  ├─ Data_for_Model_v3.csv         # Main feature dataset (panel)
│  │  └─ Data-NPL_baru.csv             # NPL dataset (optional target)
│  └─ processed/                       # (optional) cleaned/interim outputs
├─ models/                             # (optional) saved scalers/PCA/models
├─ reports/                            # (optional) figures, charts
├─ requirements.txt                    # (recommended) python dependencies
└─ README.md
```

Notes:
- Keep large CSVs out of version control or use Git LFS.
- Consider adding a `.gitignore` to exclude data/processed, models, and notebook checkpoints.

---

## 3) Data

Primary files:
- `Data_for_Model_v3.csv` (panel, quarterly):
  - Keys: `kabupaten_kota`, `tahun`, `kuartal`
  - Socioeconomic indicators (examples, Indonesian naming retained):
    - `Garis_Kemiskinan`
    - `Indeks_Pembangunan_Manusia`
    - `Persen_Penduduk_Miskin`
    - `Tingkat Pengangguran Terbuka`
    - `Upah Minimum`
    - `Jumlah Penduduk (Ribu)`
    - `Laju Pertumbuhan Penduduk per Tahun`
    - `Persentase Penduduk`
    - `Kepadatan Penduduk per km persegi (Km2)`
    - `Rasio Jenis Kelamin Penduduk`
    - `PDRB`
    - `Proksi Inflasi` (categorical label such as city proxy; not used as numeric)
    - `Laju_Inflasi`
    - `Gini_Ratio`
    - `investasi_per_kapita`
    - `Jumlah Perusahaan Kecil` (often used as a target in examples)

- `Data-NPL_baru.csv` (optional target join):
  - Keys: region name, `Tahun`, `Kuartal` (converted from strings like "Q1" to numeric)

Data provenance:
- Please document/confirm the official sources (e.g., BPS, BI, local government datasets). Insert links and access dates once finalized.

---

## 4) Methodology

### 4.1 Time-Aware Train/Test Split
- We split by time to emulate real-world forecasting.
- Example in notebook: training data consists of observations strictly before 2024 Q1; test data is 2024 Q1 and later.
- Train/test masks are constructed using `(tahun, kuartal)`.

Rationale:
- Prevents temporal leakage.
- Ensures evaluation reflects out-of-sample, forward-looking performance.

### 4.2 Handling Quarterly Constancy and Interpolation
Context:
- Several indicators are available annually but appear constant across Q1–Q4 (or sparsely populated). To avoid artificial plateaus, we:
  1) Identify years where a variable is constant within a region.
  2) Set Q2–Q4 to NaN, preserving Q1 as the anchor.
  3) Interpolate within each `kabupaten_kota` across time.

Important caution:
- In a `groupby(...).transform(...)`, relying on index modulo (e.g., `x.index % 4 == 0`) is unsafe because the index is global, not per-group. The robust approach uses the explicit `kuartal` column to identify Q2–Q4.

Leakage safety:
- Interpolation should be performed AFTER the time split, applied independently to train and test blocks, to avoid future information bleeding into training.

### 4.3 Scaling and PCA
- Standardize numeric predictors with `StandardScaler` fit on training only.
- PCA selection: choose the minimal number of components explaining > 90% cumulative variance (based on training set).
- Transform both training and test using the scaler and PCA fitted on training.

Interpretability:
- We compute and inspect PCA loadings to understand which original indicators contribute most to each component.
- Typical themes observed (example from current loadings, may evolve):
  - PC1: Prosperity/urbanization axis (HDI, density, Gini, −poverty)
  - PC2: Economic scale (population share/size, PDRB)
  - PC3: Labor/demographics (sex ratio, unemployment)
  - PC4+: Investment-driven factors and inequality nuances

### 4.4 Correlation Analysis (Optional but Recommended)
- Correlate PCs (and/or original features) with the chosen target (`Jumlah Perusahaan Kecil` or NPL) using Pearson and Spearman.
- This helps prioritize which PCs carry predictive/monotonic signal.

---

## 5) Modeling

Intended approach (as implemented/planned in the notebook):
- Model: Gradient-boosted trees (XGBoost Regressor) for tabular regression.
- Features: PCA scores (and optionally select original features if needed).
- Target: 
  - If using internal target: `Jumlah Perusahaan Kecil`
  - If using external target: join `Data-NPL_baru.csv` to predict NPL

Evaluation:
- Primary: R², MAE on the holdout test set.
- Recommended: Time series cross-validation (expanding window) to validate stability across time.

Interpretation:
- Combine tree-based feature importance in PC space with PCA loadings to infer original-feature contributions.
- This yields a transparent story from raw indicators → PCs → model predictions.

---

## 6) How to Run

### 6.1 Environment
Create and activate a virtual environment, then install dependencies (sample):

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

A minimal `requirements.txt` could include:
```
pandas
numpy
scikit-learn
xgboost
seaborn
matplotlib
scipy
jupyter
```

### 6.2 Data Placement
- Place `Data_for_Model_v3.csv` and `Data-NPL_baru.csv` under `data/raw/` (or update paths in the notebook accordingly).

### 6.3 Run the Notebook
- Open `Notebook/Model_Train_Final.ipynb` in Jupyter or VS Code.
- Execute cells top-to-bottom.
- The notebook:
  - Loads data, applies leakage-safe preprocessing (adjust as noted),
  - Fits scaler and PCA on training data,
  - Transforms test data,
  - Shows PCA loadings, correlations, and modeling workflow (XGBoost section).

Outputs (optional):
- Save trained scaler/PCA/model via `joblib` to `models/`.
- Export transformed datasets to `data/processed/`.

---

## 7) Reproducibility

- Fit/transform strictly on training to avoid data leakage.
- Fix random seeds where applicable (`random_state=42`).
- Save artifacts (scaler, PCA, model) with versioned filenames.
- Log the selected number of PCA components and cumulative explained variance.
- Consider using a `Pipeline` (scaler → PCA → model) for end-to-end consistency.

---

## 8) Limitations and Considerations

- Data Quality: Interpolation can smooth genuine shocks; validate against known events.
- Temporal Leakage: Ensure interpolation, scaling, and PCA do not peek at future data.
- Target Ambiguity: Clearly choose and document the target (MSME vs. NPL) and ensure correct joins/keys.
- Spatial vs. Temporal Signal: PCA across pooled panel data can conflate spatial differences and temporal trends. If the goal is temporal forecasting, consider:
  - Demeaning per region (fixed effects),
  - Including region dummies in downstream models,
  - Running PCA on detrended series where appropriate.
- Categorical Features: `Proksi Inflasi` is a label, not a numeric predictor; if needed, encode appropriately.

---

## 9) Roadmap

- Add robust unit tests for preprocessing and splitting logic.
- Implement expanding-window time series cross-validation.
- Add SHAP analysis for the downstream model.
- Evaluate alternative dimensionality reduction (e.g., Factor Analysis, UMAP for exploration).
- Integrate a lightweight pipeline script (`src/`) to complement the notebook.
- Document and verify official data sources with links and retrieval dates.
- Add CI (linting, tests) and data validation checks (Great Expectations or pandera).

---

## 10) Citation and Acknowledgements

Please add official data source acknowledgements here once finalized:
- [Insert Institution Name], dataset: [Title], accessed on [Date].
- [Insert any collaborators or agencies].

---

## 11) License

TBD. Consider adding a LICENSE file (e.g., MIT) to clarify reuse.

---

## 12) Contact

Maintainer: @raindragon14

For questions, issues, or collaboration proposals, please open an issue (if available) or reach out directly.

---
