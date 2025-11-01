"""
Child Observation Data Cleaning Pipeline with LLM Enhancement (OpenAI GPT-3.5-Turbo)
===============================================================================
This script cleans and standardizes child observation data from raw_observations.txt
and uses OpenAI GPT-3.5-Turbo LLM to generate three new columns:

1. Emotional_Regulation_Score (scale 1–5)
2. Social_Integration_Score (scale 1–5)
3. Resilience_Notes_Summary (short descriptive field)

Installation:
pip install pandas python-dateutil openai python-dotenv

Setup:
1. Create a .env file in the same directory with your OpenAI API key:
   OPENAI_API_KEY=your_api_key_here
2. Ensure raw_observations.txt is in the same directory

"""

import pandas as pd
import re
import json
import os
from datetime import datetime
from dateutil import parser as date_parser
import warnings
warnings.filterwarnings('ignore')

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai not installed. Please run: pip install openai")
    exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Please run: pip install python-dotenv")
    exit(1)

def load_openai_client():
    """
    Load OpenAI API key from .env file and initialize client.
    Returns:
    --------
    OpenAI: OpenAI client instance
    Raises:
    -------
    ValueError: If OPENAI_API_KEY is not found in .env file
    """
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError(
            "ERROR: OPENAI_API_KEY not found in .env file. "
            "Please create a .env file with: OPENAI_API_KEY=your_key_here"
        )
    print("[OpenAI] Initializing OpenAI client...")
    client = OpenAI(api_key=api_key)
    print(" ✓ OpenAI client initialized successfully\n")
    return client

def standardize_child_id(child_id):
    """
    Standardize Child_ID format.
    Transformations:
    - Convert to uppercase
    - Remove hyphens
    - Handle multiple IDs by taking first one
    - Strip extra whitespace
    - Replace missing values with 'UNKNOWN'
    """
    if pd.isna(child_id) or str(child_id).strip() == '':
        return 'UNKNOWN'
    child_id_str = str(child_id).strip()
    if ';' in child_id_str:
        child_id_str = child_id_str.split(';')[0].strip()
    child_id_str = child_id_str.upper().replace('-', '').strip()
    return child_id_str

def parse_session_date(date_str):
    """
    Parse Session_Date in various formats to standardized datetime.
    Supported formats:
    - YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD, YYYY.MM.DD
    - DD-MM-YYYY, MM-DD-YYYY, DD Mon YYYY, Mon DD YYYY
    - Mon DD, YYYY, DD Mon, Mon DD
    """
    if pd.isna(date_str) or str(date_str).strip() == '':
        return None
    date_str = str(date_str).strip()
    if date_str.lower() == 'last weekend':
        return None
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    date_str = re.sub(r'\s+\d{1,2}:\d{2}.*', '', date_str)
    
    date_formats = [
        '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d', '%Y.%m.%d',
        '%d-%m-%Y', '%m-%d-%Y', '%d %b %Y', '%b %d %Y', '%b %d, %Y',
        '%d %b', '%b %d',
    ]
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            if parsed_date.year == 1900:
                parsed_date = parsed_date.replace(year=2025)
            return parsed_date
        except ValueError:
            continue
    try:
        parsed_date = date_parser.parse(date_str, dayfirst=True)
        if parsed_date.year == 1900:
            parsed_date = parsed_date.replace(year=2025)
        return parsed_date
    except:
        return None

def clean_observation_text(text):
    """
    Clean observation text for standardization.
    Transformations:
    - Strip whitespace
    - Replace em-dashes with regular dashes
    - Replace shorthand (w/ → with, w/o → without)
    - Remove bullet point markers
    - Replace newlines with spaces
    - Normalize multiple spaces to single space
    - Capitalize first letter
    """
    if pd.isna(text):
        return ''
    text = str(text).strip()
    text = text.replace('—', '-')
    text = re.sub(r'\bw/\b', 'with', text)
    text = re.sub(r'\bw/o\b', 'without', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'^\s*[-•*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*[-•*+]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 0:
        text = text[0].upper() + text[1:]
    return text.strip()

def analyze_observation_with_openai(observation_text, client):
    """
    Use OpenAI GPT-3.5-Turbo to analyze observation text and generate scores.
    Parameters:
    -----------
    observation_text : str
        The cleaned observation text to analyze
    client : OpenAI
        The initialized OpenAI client
    Returns:
    --------
    dict: Contains emotional_regulation_score, social_integration_score, resilience_notes_summary
    """
    prompt = f"""You are an expert child development analyst. Based on the following observation text about a child, provide three assessments in JSON format.

Observation: {observation_text}

Provide your response ONLY as valid JSON (no other text before or after) in this exact format:

{{
"emotional_regulation_score": ,
"social_integration_score": ,
"resilience_notes_summary": ""
}}

Guidelines:
- Emotional_Regulation_Score (1-5): 1=very poor, 5=excellent. Assess ability to manage emotions, stay calm, handle frustration.
- Social_Integration_Score (1-5): 1=very poor, 5=excellent. Assess ability to interact with peers, share, cooperate, communicate.
- Resilience_Notes_Summary: Brief summary of observed resilience indicators, coping strategies, or adaptability.

Return ONLY the JSON object with no additional text."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        response_text = response.choices[0].message.content
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            result['emotional_regulation_score'] = max(1, min(5, int(result.get('emotional_regulation_score', 3))))
            result['social_integration_score'] = max(1, min(5, int(result.get('social_integration_score', 3))))
            result['resilience_notes_summary'] = str(result.get('resilience_notes_summary', 'No summary'))
            return result
        else:
            return {
                'emotional_regulation_score': 3,
                'social_integration_score': 3,
                'resilience_notes_summary': 'Unable to analyze - returned default values'
            }
    except json.JSONDecodeError:
        print(f"Warning: Could not parse OpenAI response as JSON")
        return {
            'emotional_regulation_score': 3,
            'social_integration_score': 3,
            'resilience_notes_summary': 'Parse error - returned default values'
        }
    except Exception as e:
        print(f"Warning: OpenAI analysis error: {e}")
        return {
            'emotional_regulation_score': 3,
            'social_integration_score': 3,
            'resilience_notes_summary': f'Error occurred: {str(e)}'
        }

def clean_child_observation_data_with_llm(input_file='raw_observations.txt', output_csv='cleaned_observations.csv', output_json='cleaned_observations.json'):
    """
    Main ETL pipeline for child observation data cleaning with OpenAI LLM enhancement.
    Applies cleaning steps and uses OpenAI GPT-3.5-Turbo to generate three new columns:
    1. Emotional_Regulation_Score
    2. Social_Integration_Score
    3. Resilience_Notes_Summary

    Parameters:
    -----------
    input_file : str, default='raw_observations.txt'
        Path to input CSV/TXT file with raw data
    output_csv : str, default='cleaned_observations.csv'
        Path to output CSV file
    output_json : str, default='cleaned_observations.json'
        Path to output JSON file

    Returns:
    --------
    pd.DataFrame: Enhanced dataframe with LLM-generated columns
    """
    client = load_openai_client()
    df = pd.read_csv(input_file)

    print("=" * 80)
    print("DATA CLEANING & LLM ENHANCEMENT PIPELINE (OpenAI GPT-3.5-Turbo)")
    print("=" * 80)
    print(f"\nInput file: {input_file}")
    print(f"Input rows: {len(df)}\n")

    df_cleaned = df.copy()

    print("[1/4] Standardizing Child_ID...")
    df_cleaned['Child_ID'] = df_cleaned['Child_ID'].apply(standardize_child_id)
    unknown_count = (df_cleaned['Child_ID'] == 'UNKNOWN').sum()
    print(f" ✓ {unknown_count} missing/unknown IDs filled with 'UNKNOWN'")
    print(f" ✓ Unique Child IDs: {df_cleaned['Child_ID'].nunique()}\n")

    print("[2/4] Parsing Session_Date...")
    df_cleaned['Session_Date'] = df_cleaned['Session_Date'].apply(parse_session_date)
    unparseable_count = df_cleaned['Session_Date'].isna().sum()
    print(f" ✓ Standardized to YYYY-MM-DD format")
    print(f" ✓ {unparseable_count} dates could not be parsed\n")

    print("[3/4] Cleaning Observation_Text...")
    df_cleaned['Observation_Text'] = df_cleaned['Observation_Text'].apply(clean_observation_text)
    print(f" ✓ Removed bullet points and newlines")
    print(f" ✓ Standardized formatting\n")

    print("[4/4] Analyzing observations with OpenAI GPT-3.5-Turbo...")
    emotional_scores = []
    social_scores = []
    resilience_summaries = []
    total_rows = len(df_cleaned)

    for idx, row in df_cleaned.iterrows():
        observation = row['Observation_Text']
        if pd.isna(observation) or str(observation).strip() == '':
            emotional_scores.append(3)
            social_scores.append(3)
            resilience_summaries.append('No observation data provided')
        else:
            result = analyze_observation_with_openai(observation, client)
            emotional_scores.append(result['emotional_regulation_score'])
            social_scores.append(result['social_integration_score'])
            resilience_summaries.append(result['resilience_notes_summary'])
        if (idx + 1) % 5 == 0:
            print(f" ✓ Processed {idx + 1}/{total_rows} rows")

    df_cleaned['Emotional_Regulation_Score'] = emotional_scores
    df_cleaned['Social_Integration_Score'] = social_scores
    df_cleaned['Resilience_Notes_Summary'] = resilience_summaries
    print(f" ✓ LLM analysis complete\n")

    print("[5/5] Final validation and formatting...")
    df_cleaned['Session_Date'] = df_cleaned['Session_Date'].dt.strftime('%Y-%m-%d')
    df_cleaned['Session_Date'] = df_cleaned['Session_Date'].replace('NaT', '')
    print(f" ✓ Output rows: {len(df_cleaned)}\n")

    df_cleaned.to_csv(output_csv, index=False, quoting=1)
    print(f"✓ SUCCESS: Enhanced data saved to '{output_csv}'")

    df_cleaned.to_json(output_json, orient='records', indent=2)
    print(f"✓ JSON backup saved to '{output_json}'\n")

    print("=" * 80)
    print("ENHANCEMENT SUMMARY")
    print("=" * 80)
    print(f"\nUnique Child IDs: {df_cleaned['Child_ID'].nunique()}")

    dates = df_cleaned[df_cleaned['Session_Date'] != '']['Session_Date'].sort_values()
    if len(dates) > 0:
        print(f"Date range: {dates.iloc[0]} to {dates.iloc[-1]}")

    print(f"\nLLM-Generated Scores Summary:")
    print(f" Emotional_Regulation_Score - Mean: {df_cleaned['Emotional_Regulation_Score'].mean():.2f}, Range: {df_cleaned['Emotional_Regulation_Score'].min()}-{df_cleaned['Emotional_Regulation_Score'].max()}")
    print(f" Social_Integration_Score - Mean: {df_cleaned['Social_Integration_Score'].mean():.2f}, Range: {df_cleaned['Social_Integration_Score'].min()}-{df_cleaned['Social_Integration_Score'].max()}")
    print(f"\nChild_ID distribution:")
    print(df_cleaned['Child_ID'].value_counts().to_string())
    print("\n" + "=" * 80)

    return df_cleaned

if __name__ == "__main__":
    df_enhanced = clean_child_observation_data_with_llm()
