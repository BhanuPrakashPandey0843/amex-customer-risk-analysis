"""
Enterprise Data Audit Module for American Express CFPB Risk Intelligence Analysis
Author: Senior Data Analytics Consultant
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Tuple, List
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data(file_path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Loads the CFPB dataset from Excel file.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        tuple: (DataFrame, metadata_dict)
    """
    try:
        logger.info(f"Loading dataset from {file_path}")
        df = pd.read_excel(file_path, engine='openpyxl')
        logger.info(f"Successfully loaded dataset with {len(df)} rows and {len(df.columns)} columns")
        
        metadata = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
        return df, metadata
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        raise

def generate_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates metadata report for the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame containing metadata information
    """
    metadata_rows = []
    for col in df.columns:
        sample_vals = df[col].dropna().head(5).tolist()
        metadata_rows.append({
            "Column Name": col,
            "Data Type": str(df[col].dtype),
            "Non-Null Count": df[col].count(),
            "Missing Count": df[col].isna().sum(),
            "Missing Percentage": round((df[col].isna().sum() / len(df)) * 100, 2),
            "Unique Values": df[col].nunique(),
            "Sample Values": str(sample_vals)
        })
    return pd.DataFrame(metadata_rows)

def audit_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs structural audit of the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary of structural audit findings
    """
    logger.info("Starting schema audit")
    findings = {}
    
    findings["total_rows"] = len(df)
    findings["total_columns"] = len(df.columns)
    findings["duplicate_columns"] = df.columns.duplicated().sum()
    findings["duplicate_rows"] = df.duplicated().sum()
    findings["empty_rows"] = (df.isna().all(axis=1)).sum()
    
    logger.info(f"Schema audit complete: {findings}")
    return findings

def audit_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes missing values in the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with missing value analysis
    """
    missing_analysis = []
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = round((missing_count / len(df)) * 100, 2)
        missing_analysis.append({
            "Column": col,
            "Missing Count": missing_count,
            "Missing Percentage": missing_pct
        })
    return pd.DataFrame(missing_analysis).sort_values("Missing Percentage", ascending=False)

def audit_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes duplicate records in the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary of duplicate analysis findings
    """
    exact_duplicates = df.duplicated().sum()
    exact_duplicate_pct = round((exact_duplicates / len(df)) * 100, 2)
    
    return {
        "exact_duplicates": exact_duplicates,
        "exact_duplicate_pct": exact_duplicate_pct
    }

def audit_categories(df: pd.DataFrame, categorical_cols: List[str]) -> Dict[str, Any]:
    """
    Profiles categorical columns in the dataset.
    
    Args:
        df: Input DataFrame
        categorical_cols: List of categorical column names
        
    Returns:
        Dictionary of categorical profiling results
    """
    category_audit = {}
    for col in categorical_cols:
        if col in df.columns:
            category_audit[col] = {
                "unique_values": df[col].nunique(),
                "top_5_values": df[col].value_counts().head(5).to_dict(),
                "missing_pct": round((df[col].isna().sum() / len(df)) * 100, 2)
            }
    return category_audit

def audit_dates(df: pd.DataFrame, date_cols: List[str]) -> Dict[str, Any]:
    """
    Audits date columns in the dataset.
    
    Args:
        df: Input DataFrame
        date_cols: List of date column names
        
    Returns:
        Dictionary of date audit results
    """
    date_audit = {}
    for col in date_cols:
        if col in df.columns:
            # Try to parse dates
            try:
                parsed = pd.to_datetime(df[col], errors='coerce', utc=True)
                date_audit[col] = {
                    "min_date": parsed.min() if not pd.isna(parsed.min()) else None,
                    "max_date": parsed.max() if not pd.isna(parsed.max()) else None,
                    "invalid_dates": parsed.isna().sum()
                }
            except Exception as e:
                date_audit[col] = {"error": str(e)}
    return date_audit

def calculate_quality_scores(df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    """
    Calculates quality scores for each column and overall.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Tuple of (quality_scores_df, overall_score)
    """
    scores = []
    for col in df.columns:
        completeness = 10 - (df[col].isna().sum() / len(df)) * 10
        completeness = max(1, min(10, completeness))
        
        uniqueness = 10 if col == "Complaint ID" else 5  # Simplified scoring
        uniqueness = max(1, min(10, uniqueness))
        
        score = round((completeness + uniqueness) / 2, 1)
        scores.append({
            "Column": col,
            "Completeness Score": round(completeness, 1),
            "Uniqueness Score": uniqueness,
            "Overall Score": score
        })
    
    scores_df = pd.DataFrame(scores)
    overall_score = round(scores_df["Overall Score"].mean(), 1)
    return scores_df, overall_score

def generate_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates a comprehensive audit summary.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary of summary findings
    """
    schema_audit = audit_schema(df)
    missing_audit = audit_missing_values(df)
    duplicate_audit = audit_duplicates(df)
    quality_scores, overall_score = calculate_quality_scores(df)
    
    return {
        "schema": schema_audit,
        "missing_values": missing_audit.to_dict('records'),
        "duplicates": duplicate_audit,
        "quality_scores": quality_scores.to_dict('records'),
        "overall_quality_score": overall_score,
        "companies": df["Company"].nunique(),
        "products": df["Product"].nunique(),
        "date_range": {
            "min": df["Date received"].min(),
            "max": df["Date received"].max()
        }
    }

def save_all_reports(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Saves all audit reports to the specified directory.
    
    Args:
        df: Input DataFrame
        output_dir: Output directory for reports
    """
    # Save metadata
    metadata = generate_metadata(df)
    metadata.to_csv(output_dir / "metadata_summary.csv", index=False)
    
    # Save missing values
    missing = audit_missing_values(df)
    missing.to_csv(output_dir / "missing_values_analysis.csv", index=False)
    
    # Save quality scores
    quality_scores, overall_score = calculate_quality_scores(df)
    quality_scores.to_csv(output_dir / "quality_scores.csv", index=False)
    
    # Generate summary
    summary = generate_summary(df)
    summary_df = pd.DataFrame([
        {"Metric": "Total Rows", "Value": summary["schema"]["total_rows"]},
        {"Metric": "Total Columns", "Value": summary["schema"]["total_columns"]},
        {"Metric": "Duplicate Rows", "Value": summary["schema"]["duplicate_rows"]},
        {"Metric": "Empty Rows", "Value": summary["schema"]["empty_rows"]},
        {"Metric": "Overall Quality Score", "Value": summary["overall_quality_score"]},
        {"Metric": "Unique Companies", "Value": summary["companies"]},
        {"Metric": "Unique Products", "Value": summary["products"]},
    ])
    summary_df.to_csv(output_dir / "audit_summary.csv", index=False)
    
    logger.info(f"All reports saved to {output_dir}")

if __name__ == "__main__":
    # Test the functions
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "raw" / "CFPB Complaints Data - Jan25 to Mar26.xlsx"
    output_dir = project_root / "data" / "processed"
    
    df, meta = load_data(data_path)
    print("\n=== Dataset Overview ===")
    print(meta)
    
    print("\n=== First 5 Rows ===")
    print(df.head())
    
    print("\n=== Columns ===")
    print(df.columns.tolist())
    
    print("\n=== Data Types ===")
    print(df.dtypes)
    
    print("\n=== Missing Values ===")
    missing_df = audit_missing_values(df)
    print(missing_df)
    
    print("\n=== Quality Scores ===")
    quality_scores, overall_score = calculate_quality_scores(df)
    print(quality_scores)
    print(f"\nOverall Quality Score: {overall_score} / 10")
    
    print("\n=== Saving Reports ===")
    save_all_reports(df, output_dir)
    print("Reports saved to data/processed/")

