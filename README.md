# PGL Session Insights

A comprehensive data structuring and analysis pipeline for converting unstructured facilitator notes into actionable child growth insights.

## Overview

This project automates the collection, cleaning, and analysis of weekly observation data from PGL facilitators. It transforms raw qualitative notes into structured data with AI-powered emotional regulation and social integration scoring.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Run the Pipeline

```bash
python scripts/clean_facilitator_notes.py
```

## Project Structure

```
pgl-session-insights/
├── data/
│   ├── raw/
│   │   └── raw_observations.txt       # Raw facilitator notes
│   └── processed/
│       ├── cleaned_observations.csv   # Cleaned dataset with scores
│       └── cleaned_observations.json  # JSON backup
├── scripts/
│   ├── clean_facilitator_notes.py     # Main cleaning pipeline with LLM
│   └── generate_summary_reports.py    # Analytics and aggregations
├── outputs/
│   ├── figures/                       # Charts and visualizations
│   └── tables/
│       └── summary_by_child.csv       # Aggregated metrics
├── dashboard/
│   └── powerbi/
│       └── PGL_Session_Dashboard.pbix # Power BI dashboard
└── docs/
    ├── scoring_rules.md               # Scoring methodology
    ├── README_DATA.md                 # Data schema & definitions
    └── ASSUMPTIONS.md                 # Caveats & synthetic data notes
```

## Pipeline Overview

### Input: Raw Facilitator Notes
```
Child_ID, Session_Date, Observation_Text
C001, 2025-10-20, "Child was quiet during group work but smiled when helping peers."
C002, 2025-10-21, "Child got frustrated after losing the game but rejoined after 5 minutes."
```

### Processing Steps
1. **Data Cleaning** – Standardize IDs, parse dates, normalize text
2. **LLM Analysis** – Use OpenAI GPT-3.5-Turbo to generate:
   - Emotional_Regulation_Score (1–5)
   - Social_Integration_Score (1–5)
   - Resilience_Notes_Summary (short descriptive field)
3. **Output** – CSV and JSON formats for BI and downstream analysis

### Output: Structured Dataset
```
Child_ID, Session_Date, Observation_Text, Emotional_Regulation_Score, Social_Integration_Score, Resilience_Notes_Summary
C001, 2025-10-20, "Child was quiet during...", 3, 4, "Collaborative helper with moderate self-expression"
```

## Key Features

- **Automated Scoring** – AI-powered analysis eliminates manual tagging
- **Error Handling** – Graceful fallbacks for parsing and API errors
- **Modular Design** – Easy to extend with new functions
- **Progress Tracking** – Real-time feedback during processing
- **Summary Statistics** – Automatic generation of key metrics

## Usage

### Command Line
```bash
python scripts/clean_facilitator_notes.py
```

### Python Import
```python
from scripts.clean_facilitator_notes import clean_child_observation_data_with_llm

df = clean_child_observation_data_with_llm(
    input_file='data/raw/raw_observations.txt',
    output_csv='data/processed/cleaned_observations.csv',
    output_json='data/processed/cleaned_observations.json'
)
```

## Data Schema

| Column | Type | Description |
|--------|------|-------------|
| Child_ID | String | Unique child identifier (standardized uppercase) |
| Session_Date | Date | YYYY-MM-DD formatted session date |
| Observation_Text | String | Cleaned, normalized facilitator observation |
| Emotional_Regulation_Score | Integer | Scale 1–5 (1=very poor, 5=excellent) |
| Social_Integration_Score | Integer | Scale 1–5 (1=very poor, 5=excellent) |
| Resilience_Notes_Summary | String | Brief descriptive summary of resilience indicators |

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies: pandas, python-dateutil, openai, python-dotenv

See `requirements.txt` for full list.

## Output Files

- `data/processed/cleaned_observations.csv` – Main cleaned dataset
- `data/processed/cleaned_observations.json` – JSON format backup
- `outputs/tables/summary_by_child.csv` – Aggregated metrics by child
- `outputs/figures/` – Charts and visualizations for dashboards

## Documentation

- **[scoring_rules.md](docs/scoring_rules.md)** – Detailed explanation of 1–5 scoring methodology
- **[README_DATA.md](docs/README_DATA.md)** – Data dictionary and column definitions
- **[ASSUMPTIONS.md](docs/ASSUMPTIONS.md)** – Important caveats and assumptions

## License

MIT License – See LICENSE file for details.

## Contact

PGL Data & Insights Team
