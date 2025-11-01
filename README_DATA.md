# Data Dictionary & Schema

## Dataset Overview

The cleaned observation dataset contains structured, AI-enhanced records of child observations from PGL facilitators. Each row represents one observation session for a child.

## Column Definitions

### Child_ID (String, Primary Key)
**Description:** Unique identifier for each child in the program.  
**Format:** Uppercase alphanumeric (e.g., C001, CHILD_A, ID_123)  
**Notes:** Standardized during cleaning (hyphens removed, uppercase applied). Missing values replaced with 'UNKNOWN'.  
**Example:** `C001`, `C002`, `UNKNOWN`

### Session_Date (Date)
**Description:** Date when the observation was recorded.  
**Format:** YYYY-MM-DD (ISO 8601)  
**Parsing:** Handles multiple input formats during cleaning (DD/MM/YYYY, MM/DD/YYYY, written text, etc.)  
**Missing:** Empty string if unparseable  
**Example:** `2025-10-20`, `2025-10-21`

### Observation_Text (String, Free Text)
**Description:** Cleaned and standardized facilitator observation notes.  
**Format:** Plain text, sentence-case  
**Cleaning:** Bullet points removed, newlines replaced with spaces, shorthand expanded (w/ → with, w/o → without), multiple spaces normalized  
**Length:** Typically 20–200 characters  
**Example:** `"Child was quiet during group work but smiled when helping peers."`

### Emotional_Regulation_Score (Integer)
**Description:** AI-generated score measuring the child's ability to manage emotions, stay calm, and handle frustration.  
**Scale:** 1–5 (1=very poor, 5=excellent)  
**Source:** OpenAI GPT-3.5-Turbo LLM analysis of Observation_Text  
**Fallback:** 3 (Moderate) if LLM analysis fails  
**Validation:** Automatically constrained to 1–5 range  
**Example:** `3`, `4`, `5`

### Social_Integration_Score (Integer)
**Description:** AI-generated score measuring the child's ability to interact with peers, share, cooperate, and communicate effectively.  
**Scale:** 1–5 (1=very poor, 5=excellent)  
**Source:** OpenAI GPT-3.5-Turbo LLM analysis of Observation_Text  
**Fallback:** 3 (Moderate) if LLM analysis fails  
**Validation:** Automatically constrained to 1–5 range  
**Example:** `3`, `4`, `5`

### Resilience_Notes_Summary (String)
**Description:** Short, AI-generated descriptive summary of observed resilience indicators, coping strategies, or adaptability.  
**Format:** 1–2 sentence description  
**Source:** OpenAI GPT-3.5-Turbo LLM analysis  
**Fallback:** "No observation data provided" or error message  
**Example:** `"Collaborative helper with moderate self-expression"`, `"Self-regulated after setback and demonstrated conflict resolution skills."`

## Data Quality Notes

### Standardization Applied
- **Child_ID:** Uppercase, hyphens removed
- **Session_Date:** Parsed to YYYY-MM-DD format; unparseable dates set to empty string
- **Observation_Text:** Normalized case, bullet points removed, shorthand expanded

### Missing Data Handling
- **Child_ID:** Replaced with 'UNKNOWN'
- **Session_Date:** Empty string if parsing fails
- **Observation_Text:** Empty string if null/missing
- **Scores:** Default to 3 (Moderate) if LLM analysis fails or text is empty

### Data Dimensions
- **Rows:** One per observation session
- **Columns:** 6 (Child_ID, Session_Date, Observation_Text, Emotional_Regulation_Score, Social_Integration_Score, Resilience_Notes_Summary)

## Export Formats

### CSV (cleaned_observations.csv)
- UTF-8 encoding
- Comma-separated values
- Headers: Child_ID, Session_Date, Observation_Text, Emotional_Regulation_Score, Social_Integration_Score, Resilience_Notes_Summary

### JSON (cleaned_observations.json)
- UTF-8 encoding
- Array of objects format
- Pretty-printed (indent=2 for readability)

### Summary CSV (summary_by_child.csv)
- Aggregated by Child_ID
- Columns: Child_ID, Session_Count, Avg_Emotional_Regulation, Avg_Social_Integration, Latest_Session_Date

## Integration with Power BI

The cleaned CSV can be imported directly into Power BI with:
- **Child_ID** as dimension (filter/slicer)
- **Session_Date** as timeline dimension
- **Emotional_Regulation_Score, Social_Integration_Score** as numeric measures
- **Resilience_Notes_Summary** as tooltip/card visual

Recommended visualizations:
- Line chart: Score trends over time by child
- Card: Average scores across program
- Heatmap: Child-by-metric matrix
- Table: Ranked children by most recent score
