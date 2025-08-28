# Risk Score and NPL Correlation Analysis Documentation

## Executive Summary

This document details the comprehensive methodology and findings of the Pearson correlation analysis between district-level risk scores (PCA-based and expert-weighted) and Non-Performing Loan (NPL) percentages in East Java Province.

## 1. Research Objective

The primary objective of this analysis is to evaluate the predictive relationship between two types of risk scores and NPL percentages across multiple time horizons:
- Current quarter (kuartal)
- One quarter ahead (kuartal+1)
- Two quarters ahead (kuartal+2)

## 2. Data Sources

### 2.1 Aggregated Risk Scores Dataset
- **File**: `Aggregated_Risk_Scores.csv`
- **Temporal Coverage**: Q1 2022 - Q4 2024 (12 quarters)
- **Geographic Coverage**: 38 districts/cities in East Java Province
- **Key Variables**:
  - `Weighted_PCA_Score`: Statistically derived risk score using Principal Component Analysis
  - `Weighted_Expert_Score`: Risk score incorporating domain expert knowledge
  - `Total_PDRB`: Gross Regional Domestic Product
  - Structural identifiers: District name, Year, Quarter

### 2.2 NPL Dataset
- **File**: `Data-NPL_baru.csv`
- **Temporal Coverage**: Q1 2020 - Q1 2025 (21 quarters)
- **Key Variable**: `NPL` - Non-Performing Loan percentage

## 3. Methodology

### 3.1 Data Preprocessing

#### 3.1.1 Data Cleaning
```python
# Convert quarter format from "Q1" to numeric 1.0
npl_df['Kuartal'] = npl_df['Kuartal'].str.replace('Q', '').astype(float)
```

#### 3.1.2 Spatial Aggregation
```python
# Calculate quarterly averages across all districts
quarterly_avg = risk_df.groupby(['Tahun', 'Kuartal']).agg({
    'Weighted_PCA_Score': 'mean',
    'Weighted_Expert_Score': 'mean'
}).reset_index()
```

#### 3.1.3 Temporal Alignment
- Inner join performed on Year and Quarter columns
- Resulting dataset: 12 quarterly observations (2022 Q1 - 2024 Q4)

### 3.2 Statistical Analysis

#### 3.2.1 Pearson Correlation
- **Statistical Package**: SciPy `pearsonr()` function
- **Formula**: 
  ```
  r = Σ[(x_i - x̄)(y_i - ȳ)] / √[Σ(x_i - x̄)² Σ(y_i - ȳ)²]
  ```

#### 3.2.2 Time Lag Analysis
Three correlation scenarios analyzed:
1. **Current Quarter**: Risk score vs same quarter NPL
2. **Quarter+1**: Risk score vs NPL one quarter ahead
3. **Quarter+2**: Risk score vs NPL two quarters ahead

#### 3.2.3 Statistical Significance
- **Null Hypothesis**: No correlation between risk scores and NPL
- **Significance Level**: α = 0.05
- **Decision Rule**: p-value < 0.05 indicates statistical significance

### 3.3 Interpretation Framework

#### Correlation Strength Guidelines:
- **Very Strong**: |r| ≥ 0.8
- **Strong**: 0.6 ≤ |r| < 0.8
- **Moderate**: 0.4 ≤ |r| < 0.6
- **Weak**: |r| < 0.4

## 4. Results

### 4.1 Weighted PCA Score vs NPL
| Time Lag | Correlation (r) | p-value | Significance | Strength |
|----------|-----------------|---------|--------------|----------|
| Current Quarter | 0.6351 | 0.0265 | Significant | Moderate |
| Quarter+1 | 0.3704 | 0.2622 | Not Significant | Weak |
| Quarter+2 | 0.2673 | 0.4554 | Not Significant | Weak |

### 4.2 Weighted Expert Score vs NPL
| Time Lag | Correlation (r) | p-value | Significance | Strength |
|----------|-----------------|---------|--------------|----------|
| Current Quarter | 0.8454 | 0.0005 | Highly Significant | Very Strong |
| Quarter+1 | 0.8055 | 0.0028 | Significant | Very Strong |
| Quarter+2 | 0.8380 | 0.0025 | Significant | Very Strong |

## 5. Detailed Analysis: Expert Score Superiority

### 5.1 Theoretical Foundations

**PCA-Based Score Limitations:**
1. **Statistical Artifact Risk**: May capture variance that is statistically significant but economically meaningless
2. **Context Blindness**: Lacks incorporation of banking industry-specific risk factors
3. **Temporal Instability**: Statistical relationships may change without economic rationale

**Expert-Based Score Advantages:**
1. **Domain Knowledge Integration**: Incorporates banking risk management expertise
2. **Economic Rationale**: Based on established risk factors affecting loan performance
3. **Regulatory Alignment**: Consistent with banking supervision frameworks

### 5.2 Empirical Evidence

**Consistency Across Time Horizons:**
- Expert Score maintains strong correlations (r = 0.8055-0.8454) across all time lags
- PCA Score correlation decays rapidly from moderate to weak

**Statistical Significance Pattern:**
- Expert Score: All correlations statistically significant (p < 0.01)
- PCA Score: Only current quarter significant, future quarters not significant

### 5.3 Practical Implications

**Expert Score Utility:**
1. **Early Warning System**: Strong predictive power for future NPL trends
2. **Resource Allocation**: Enables proactive risk mitigation measures
3. **Capital Planning**: Supports better capital adequacy planning

**PCA Score Limitations:**
1. **Limited Forecasting Value**: Weak predictive power beyond current quarter
2. **Implementation Challenges**: Difficult to explain to stakeholders
3. **Regulatory Acceptance**: May not meet supervisory expectations

## 6. Methodological Considerations

### 6.1 Strengths
- **Comprehensive Coverage**: Full geographic representation of East Java
- **Multiple Time Horizons**: Analysis of immediate and lagged effects
- **Statistical Rigor**: Proper significance testing and correlation analysis
- **Comparative Framework**: Direct comparison of statistical vs expert-based approaches

### 6.2 Limitations
- **Sample Size**: 12 quarterly observations limit statistical power
- **Time Period**: Limited to post-2022 data due to risk score availability
- **External Factors**: Cannot control for macroeconomic shocks or policy changes

## 7. Code Implementation

### 7.1 Main Analysis Script
```python
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Load data
risk_df = pd.read_csv('Aggregated_Risk_Scores.csv')
npl_df = pd.read_csv('Data-NPL_baru.csv')

# Data preprocessing
npl_df['Kuartal'] = npl_df['Kuartal'].str.replace('Q', '').astype(float)
quarterly_avg = risk_df.groupby(['Tahun', 'Kuartal']).agg({
    'Weighted_PCA_Score': 'mean',
    'Weighted_Expert_Score': 'mean'
}).reset_index()

# Merge datasets
merged_df = pd.merge(quarterly_avg, npl_df, on=['Tahun', 'Kuartal'], how='inner')

# Correlation analysis function
def calculate_correlations(data, score_col, npl_col):
    print(f'Correlation analysis for {score_col}:')
    
    # Current quarter
    corr_current, p_value_current = pearsonr(data[score_col], data[npl_col])
    print(f'Current quarter: r = {corr_current:.4f}, p-value = {p_value_current:.4f}')
    
    # Quarter+1
    if len(data) > 1:
        score_values = data[score_col].iloc[:-1].values
        npl_values = data[npl_col].iloc[1:].values
        if len(score_values) == len(npl_values):
            corr_q1, p_value_q1 = pearsonr(score_values, npl_values)
            print(f'Quarter+1: r = {corr_q1:.4f}, p-value = {p_value_q1:.4f}')
    
    # Quarter+2
    if len(data) > 2:
        score_values = data[score_col].iloc[:-2].values
        npl_values = data[npl_col].iloc[2:].values
        if len(score_values) == len(npl_values):
            corr_q2, p_value_q2 = pearsonr(score_values, npl_values)
            print(f'Quarter+2: r = {corr_q2:.4f}, p-value = {p_value_q2:.4f}')
    print()

# Execute analysis
calculate_correlations(merged_df, 'Weighted_PCA_Score', 'NPL')
calculate_correlations(merged_df, 'Weighted_Expert_Score', 'NPL')
```

## 8. Conclusion and Recommendations

### 8.1 Key Findings
1. The expert-weighted risk score demonstrates superior predictive power across all time horizons
2. PCA-based scores show limited forecasting capability beyond the current quarter
3. Expert scores maintain very strong correlations (r > 0.8) with statistical significance

### 8.2 Implementation Recommendations
1. **Adopt Expert-Weighted Scores**: For NPL forecasting and risk management
2. **Develop Early Warning Systems**: Utilize quarter+1 and quarter+2 correlations
3. **Regular Validation**: Continuously monitor and update expert weighting methodologies
4. **Integration**: Incorporate into existing risk management frameworks

### 8.3 Future Research Directions
1. Expand temporal coverage with historical data
2. Incorporate additional economic variables
3. Develop machine learning models for enhanced prediction
4. Conduct regional-specific analysis for targeted interventions

## Appendix: Data Availability Period

**Risk Scores**: Q1 2022 - Q4 2024 (12 quarters)
**NPL Data**: Q1 2020 - Q1 2025 (21 quarters)
**Analysis Period**: Q1 2022 - Q4 2024 (12 matched quarters)

---

*Documentation generated on: 2025-08-28*  
*Analysis Period: 2022 Q1 - 2024 Q4*  
*Methodology: Pearson Correlation Analysis with Time Lags*