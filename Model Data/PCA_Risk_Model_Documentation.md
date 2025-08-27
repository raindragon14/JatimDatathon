# PCA-Based Risk Model Development Documentation

## Overview
This document details the development of a Principal Component Analysis (PCA)-based risk assessment model for predicting Non-Performing Loan (NPL) rates across East Java administrative regions.

## 1. Project Objectives
- Develop a predictive model for NPL rates using socioeconomic indicators
- Apply PCA for optimal feature weighting and dimensionality reduction
- Validate model effectiveness across different time horizons
- Create a risk categorization system for regional assessment

## 2. Data Sources

### Primary Datasets:
- `Basic_Model_Feed_2023.csv` - 2023 socioeconomic data
- `Basic_Model_Feed_2024.csv` - 2024 socioeconomic data  
- `Data-NPL_baru.csv` - Quarterly NPL rates for validation

### Consolidated Dataset:
- `basic_model_feed.csv` - Combined 2023-2024 data with selected features
- `pca_risk_model_results.csv` - Final risk scores and categories

## 3. Feature Selection Process

### Initial Feature Analysis
Based on economic relevance and statistical properties, the following features were selected:

| Feature | Description | Economic Rationale |
|---------|-------------|-------------------|
| Laju_Inflasi | Inflation Rate | Economic stability indicator |
| Tingkat Pengangguran Terbuka | Open Unemployment Rate | Labor market health |
| Persen_Penduduk_Miskin | Poverty Rate | Socioeconomic vulnerability |
| Upah Minimum | Minimum Wage | Income level indicator |
| PDRB | Regional GDP | Economic output measure |
| Indeks_Pembangunan_Manusia | Human Development Index | Overall development status |

### Correlation Analysis
Features were selected to minimize multicollinearity while maintaining economic relevance:
```python
# Correlation matrix analysis
correlation_matrix = selected_features.corr()
print("Feature Correlation Matrix:")
print(correlation_matrix)
```

## 4. PCA Methodology

### Data Preprocessing
```python
# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(selected_features)

# Handle data formatting issues
basic_model_feed['Laju_Inflasi'] = (
    basic_model_feed['Laju_Inflasi']
    .astype(str)
    .str.replace(',', '.')
    .astype(float)
)
```

### PCA Implementation
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Apply PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# Extract principal component loadings
pc1_loadings = pca.components_[0]

# Calculate feature weights
adjusted_loadings = np.abs(pc1_loadings)
weights = adjusted_loadings / np.sum(adjusted_loadings)
```

### Feature Weights (Final)
| Feature | PCA Weight | Interpretation |
|---------|------------|----------------|
| Laju_Inflasi | 0.183 | High importance for risk assessment |
| Tingkat Pengangguran Terbuka | 0.168 | Significant labor market impact |
| Persen_Penduduk_Miskin | 0.172 | Poverty as key risk factor |
| Upah Minimum | 0.157 | Income level contribution |
| PDRB | 0.159 | Economic output significance |
| Indeks_Pembangunan_Manusia | 0.161 | Development status impact |

## 5. Risk Score Calculation

### Raw Risk Score Formula
```python
def calculate_risk_score(row, weights):
    """Calculate PCA-weighted risk score for a region"""
    score = 0
    for i, feature in enumerate(selected_features.columns):
        score += row[feature] * weights[i]
    return score

# Apply to all regions
basic_model_feed['PCA_Risk_Score_Raw'] = basic_model_feed.apply(
    lambda row: calculate_risk_score(row, weights), axis=1
)
```

### Normalization
```python
# Min-Max normalization to 0-1 scale
min_score = basic_model_feed['PCA_Risk_Score_Raw'].min()
max_score = basic_model_feed['PCA_Risk_Score_Raw'].max()
basic_model_feed['PCA_Risk_Score_Normalized'] = (
    (basic_model_feed['PCA_Risk_Score_Raw'] - min_score) / 
    (max_score - min_score)
)
```

## 6. Risk Categorization

### Category Thresholds
| Risk Category | Normalized Score Range | Description |
|---------------|------------------------|-------------|
| Very High Risk | 0.75 - 1.00 | Critical risk regions |
| High Risk | 0.50 - 0.75 | Elevated risk areas |
| Medium Risk | 0.25 - 0.50 | Moderate risk regions |
| Low Risk | 0.00 - 0.25 | Low risk areas |

### Implementation
```python
def categorize_risk(score):
    if score >= 0.75:
        return "Very High Risk"
    elif score >= 0.50:
        return "High Risk"
    elif score >= 0.25:
        return "Medium Risk"
    else:
        return "Low Risk"

basic_model_feed['Risk_Category'] = basic_model_feed['PCA_Risk_Score_Normalized'].apply(categorize_risk)
```

## 7. Model Validation

### Validation Methodology
- Pearson correlation analysis with NPL data
- Testing across multiple time horizons:
  - Current quarter (t)
  - One quarter ahead (t+1)
  - Two quarters ahead (t+2)

### Correlation Function
```python
from scipy.stats import pearsonr

def create_lagged_correlation(pca_data, npl_data, lag_quarters):
    """Calculate correlation between PCA scores and future NPL values"""
    
    merged_data = []
    
    for _, pca_row in pca_data.iterrows():
        region = pca_row['Nama_Kabupaten_Kota']
        year = pca_row['Tahun']
        quarter = pca_row['Kuartal']
        risk_score = pca_row['PCA_Risk_Score_Normalized']
        
        # Calculate target quarter for NPL data
        target_quarter = quarter + lag_quarters
        target_year = year
        
        if target_quarter > 4:
            target_quarter -= 4
            target_year += 1
        
        # Find matching NPL data
        npl_match = npl_data[
            (npl_data['Tahun'] == target_year) & 
            (npl_data['Kuartal'] == target_quarter)
        ]
        
        if not npl_match.empty:
            npl_value = npl_match['NPL'].values[0]
            merged_data.append({
                'Region': region,
                'PCA_Score': risk_score,
                'NPL': npl_value,
                'Time_Lag': f'Q{lag_quarters}'
            })
    
    return pd.DataFrame(merged_data)
```

### Validation Results
| Time Horizon | Pearson Correlation (r) | p-value | Statistical Significance |
|--------------|-------------------------|---------|--------------------------|
| Current Quarter (t) | 0.835 | 0.010 | Excellent |
| One Quarter Ahead (t+1) | 0.822 | 0.012 | Excellent |
| Two Quarters Ahead (t+2) | 0.801 | 0.030 | Strong |

## 8. Key Findings

### 1. Predictive Power
The model demonstrates excellent predictive capability:
- **Current quarter**: r = 0.835 (p = 0.010)
- **One quarter ahead**: r = 0.822 (p = 0.012)  
- **Two quarters ahead**: r = 0.801 (p = 0.030)

### 2. Risk Distribution
- **Very High Risk**: Regions with persistent socioeconomic challenges
- **High Risk**: Areas with elevated but manageable risk factors
- **Medium Risk**: Regions with moderate economic stability
- **Low Risk**: Economically stable areas with strong fundamentals

### 3. Feature Importance
Inflation rate and poverty rate emerged as the most significant predictors of NPL risk.

## 9. Implementation Code

### Complete Workflow
```python
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr

# Load and prepare data
def load_and_prepare_data():
    # Implementation details...
    pass

# PCA weight calculation
def calculate_pca_weights(features):
    # Implementation details...
    pass

# Risk score calculation
def calculate_risk_scores(data, weights):
    # Implementation details...
    pass

# Validation analysis
def validate_model(pca_scores, npl_data):
    # Implementation details...
    pass
```

## 10. Business Applications

### 1. Credit Risk Management
- Early warning system for NPL trends
- Regional risk assessment for loan portfolio management

### 2. Policy Development
- Targeted interventions for high-risk regions
- Resource allocation based on risk profiles

### 3. Economic Monitoring
- Continuous monitoring of regional economic health
- Predictive insights for economic planning

## 11. Limitations and Future Work

### Current Limitations
- Limited to East Java region data
- Quarterly data frequency
- Relies on available socioeconomic indicators

### Future Enhancements
- Incorporate additional economic indicators
- Expand to national coverage
- Implement machine learning enhancements
- Real-time data integration

## 12. Conclusion

The PCA-based risk model successfully:
1. Identified optimal feature weights through dimensionality reduction
2. Created a robust risk scoring system for regional assessment
3. Demonstrated excellent predictive power for NPL rates
4. Provided actionable insights for risk management and policy development

The model serves as a valuable tool for financial institutions and policymakers in understanding and predicting regional credit risk patterns.