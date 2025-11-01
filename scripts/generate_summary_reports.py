"""
Generate summary reports and aggregations from cleaned observation data.
Produces CSV exports and chart assets for Power BI dashboard integration.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

def generate_summary_by_child(input_csv='data/processed/cleaned_observations.csv', output_csv='outputs/tables/summary_by_child.csv'):
    """
    Aggregate cleaned observations by Child_ID to produce summary metrics.
    Outputs: Child_ID, Session_Count, Avg_Emotional_Regulation, Avg_Social_Integration, Latest_Session_Date
    """
    df = pd.read_csv(input_csv)
    summary = df.groupby('Child_ID').agg({
        'Session_Date': ['count', 'max'],
        'Emotional_Regulation_Score': 'mean',
        'Social_Integration_Score': 'mean',
    }).round(2)
    summary.columns = ['Session_Count', 'Latest_Session_Date', 'Avg_Emotional_Regulation', 'Avg_Social_Integration']
    summary = summary.reset_index()
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    summary.to_csv(output_csv, index=False)
    print(f"✓ Summary by child saved to {output_csv}")
    return summary

def generate_score_distribution_chart(input_csv='data/processed/cleaned_observations.csv', output_path='outputs/figures/score_distribution.png'):
    """
    Create histograms showing distribution of Emotional_Regulation and Social_Integration scores.
    """
    df = pd.read_csv(input_csv)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    df['Emotional_Regulation_Score'].hist(bins=5, ax=axes[0], color='#4CAF50', edgecolor='black')
    axes[0].set_title('Emotional Regulation Score Distribution', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Score (1-5)')
    axes[0].set_ylabel('Frequency')
    
    df['Social_Integration_Score'].hist(bins=5, ax=axes[1], color='#2196F3', edgecolor='black')
    axes[1].set_title('Social Integration Score Distribution', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Score (1-5)')
    axes[1].set_ylabel('Frequency')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Score distribution chart saved to {output_path}")
    plt.close()

def generate_trends_by_child_chart(input_csv='data/processed/cleaned_observations.csv', output_path='outputs/figures/trends_by_child.png'):
    """
    Create a heatmap showing average scores by child.
    """
    df = pd.read_csv(input_csv)
    summary = df.groupby('Child_ID')[['Emotional_Regulation_Score', 'Social_Integration_Score']].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(summary, annot=True, fmt='.2f', cmap='RdYlGn', vmin=1, vmax=5, cbar_kws={'label': 'Score'}, ax=ax)
    ax.set_title('Average Scores by Child', fontsize=14, fontweight='bold')
    ax.set_ylabel('Child ID')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Trends by child heatmap saved to {output_path}")
    plt.close()

def generate_all_reports(input_csv='data/processed/cleaned_observations.csv'):
    """
    Master function to generate all summary reports and charts.
    """
    print("=" * 80)
    print("GENERATING SUMMARY REPORTS AND CHARTS")
    print("=" * 80 + "\n")
    
    generate_summary_by_child(input_csv)
    generate_score_distribution_chart(input_csv)
    generate_trends_by_child_chart(input_csv)
    
    print("\n" + "=" * 80)
    print("All reports generated successfully!")
    print("=" * 80)

if __name__ == "__main__":
    generate_all_reports()
