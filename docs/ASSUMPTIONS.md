# Key Assumptions & Caveats

## Data & Methodology

### 1. Facilitator Note Quality
**Assumption:** Facilitator notes are specific, objective, and behavior-focused.  
**Caveat:** Vague notes (e.g., "seemed upset") will yield less precise AI scores than detailed observations (e.g., "yelled and threw blocks"). Regular facilitator training recommended.

### 2. LLM Interpretation
**Assumption:** OpenAI GPT-3.5-Turbo accurately interprets child development indicators.  
**Caveat:** LLM may miss cultural or contextual nuances. Occasional human review (especially for scores 1–2 and 4–5 extremes) recommended.

### 3. Score Generalization
**Assumption:** A single observation represents typical child behavior.  
**Caveat:** One session does not define a child. Scores should be viewed as snapshots. Trends over multiple sessions are more meaningful than individual observations.

### 4. Scale Neutrality
**Assumption:** Scoring is unbiased across all children.  
**Caveat:** Facilitator expectations, biases, or familiarity with a child may subtly influence observation language (e.g., "typically quiet" vs. "painfully shy"). Blind review of anonymized samples recommended.

## Data Collection

### 5. Session Frequency
**Assumption:** All children have similar observation frequency.  
**Caveat:** Children attending fewer sessions will have fewer data points. Comparison across children with vastly different attendance should be done cautiously.

### 6. Date Parsing
**Assumption:** Dates are in a recognizable format.  
**Caveat:** Ambiguous formats (e.g., "01/02/2025") are parsed with dayfirst=True. If a different locale is expected, manual date review is recommended.

### 7. Missing Data
**Assumption:** Missing child IDs, dates, or empty observation text are data quality issues, not meaningful absences.  
**Caveat:** Unknown child IDs are grouped together; empty observations default to score 3 (Moderate). This may mask legitimate data gaps.

## Scoring & Interpretation

### 8. 1–5 Scale Validity
**Assumption:** A 1–5 scale adequately captures the range of emotional regulation and social integration in this age group (9–12).  
**Caveat:** Finer granularity (e.g., 1–10) might better differentiate children, but 1–5 is simpler for facilitators to interpret.

### 9. Independence of Dimensions
**Assumption:** Emotional Regulation and Social Integration are independent constructs.  
**Caveat:** In practice, they are correlated (e.g., children with high emotional regulation often have high social integration). Interpret them as distinct but related.

### 10. One-Off Outbursts
**Assumption:** Fleeting emotional reactions are contextualized (e.g., loss, frustration) and not permanent.  
**Caveat:** An isolated outburst may temporarily lower Emotional Regulation score. Trend analysis (not single-session scores) is recommended for developmental insights.

## Dashboard & Reporting

### 11. Aggregation Bias
**Assumption:** Averaging scores by child is meaningful.  
**Caveat:** Mean scores can mask variability. A child with scores [2, 5, 2, 5] averages to 3.5 but shows high volatility. Include variance/SD in reporting when possible.

### 12. Real vs. Synthetic Data
**Assumption:** This project uses real facilitator notes for scoring.  
**Caveat:** If example data or mock data is used for testing, results are illustrative only and should not inform actual program decisions.

### 13. Generalizability
**Assumption:** Scores can be compared across cohorts or programs using this pipeline.  
**Caveat:** Facilitator style, child demographics, and session context may differ. Comparisons across very different groups should include contextual notes.

## Recommendations for Improvement

1. **Facilitator Training:** Standardize observation language and frequency.
2. **Human Validation:** Quarterly review of LLM scores vs. facilitator intent.
3. **Trend Analysis:** Use multi-week trend lines rather than single-session snapshots.
4. **Contextual Notes:** Capture external factors (e.g., illness, family stress) that may influence scores.
5. **Longitudinal Tracking:** Build models to predict growth trajectories, not just current state.
