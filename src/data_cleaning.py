"""
Enterprise Data Cleaning Module for American Express CFPB Risk Intelligence Analysis
Author: Principal Data Engineer
"""
import pandas as pd
import numpy as np
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/processed/cleaning_log.csv'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Company standardization mapping
COMPANY_MAPPING = {
    'AMERICAN EXPRESS COMPANY': 'American Express',
    'AMERICAN EXPRESS': 'American Express',
    'JPMORGAN CHASE & CO.': 'JPMorgan Chase',
    'CHASE': 'JPMorgan Chase',
    'BANK OF AMERICA, NATIONAL ASSOCIATION': 'Bank of America',
    'CITIBANK, N.A.': 'Citibank',
    'WELLS FARGO & COMPANY': 'Wells Fargo',
    'CAPITAL ONE FINANCIAL CORPORATION': 'Capital One',
    'U.S. BANCORP': 'U.S. Bank',
    'BARCLAYS BANK DELAWARE': 'Barclays',
    'SYNCHRONY FINANCIAL': 'Synchrony Financial'
}

def load_data(file_path: Path) -> pd.DataFrame:
    """
    Load raw CFPB dataset.
    """
    logger.info(f"Loading raw data from {file_path}")
    df = pd.read_excel(file_path, engine='openpyxl')
    logger.info(f"Raw data loaded: {len(df):,} rows, {len(df.columns)} columns")
    return df

def clean_text_column(series: pd.Series) -> pd.Series:
    """
    Clean text columns: strip whitespace, normalize.
    """
    if pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
        return series.str.strip()
    return series

def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse and standardize date fields.
    """
    logger.info("Cleaning date fields")
    df = df.copy()
    df['Date received'] = pd.to_datetime(df['Date received'], errors='coerce', utc=True)
    logger.info(f"Dates parsed: {df['Date received'].isna().sum()} invalid")
    return df

def standardize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize categorical fields.
    """
    logger.info("Standardizing categories")
    df = df.copy()

    # Standardize companies
    df['Company'] = df['Company'].replace(COMPANY_MAPPING)
    logger.info(f"Company standardized to {df['Company'].nunique()} unique values")

    # Handle missing values
    df['Sub-issue'] = df['Sub-issue'].fillna('Not specified')
    df['State'] = df['State'].fillna('Not specified')

    return df

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer analytical features.
    """
    logger.info("Engineering features")
    df = df.copy()

    # Date features
    df['Complaint Year'] = df['Date received'].dt.year
    df['Complaint Quarter'] = df['Date received'].dt.quarter
    df['Complaint Month'] = df['Date received'].dt.month
    df['Complaint Month Name'] = df['Date received'].dt.month_name()
    df['Complaint Week'] = df['Date received'].dt.isocalendar().week
    df['Complaint Day'] = df['Date received'].dt.dayofweek
    df['Complaint Day Name'] = df['Date received'].dt.day_name()

    # Binary flags
    df['Timely Response Flag'] = (df['Timely response?'] == 'Yes').astype(int)

    # Product grouping
    product_groups = {
        'Credit card': 'Cards',
        'Prepaid card': 'Cards',
        'Checking or savings account': 'Accounts',
        'Money transfer, virtual currency, or money service': 'Payments',
        'Credit reporting or other personal consumer reports': 'Credit Reporting',
        'Debt collection': 'Collections',
        'Mortgage': 'Loans',
        'Vehicle loan or lease': 'Loans',
        'Payday loan, title loan, personal loan, or advance loan': 'Loans',
        'Debt or credit management': 'Services'
    }
    df['Product Group'] = df['Product'].map(product_groups).fillna('Other')

    return df

def validate_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate cleaned dataset.
    """
    logger.info("Validating dataset")
    issues = []

    # Check Complaint ID uniqueness
    if df['Complaint ID'].nunique() != len(df):
        issues.append("Complaint ID not unique")

    # Check critical fields not missing
    critical_fields = ['Date received', 'Company', 'Product', 'Issue', 'Complaint ID']
    for field in critical_fields:
        if df[field].isna().sum() > 0:
            issues.append(f"{field} has missing values")

    is_valid = len(issues) == 0
    return is_valid, issues

def export_clean_dataset(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Export cleaned dataset.
    """
    logger.info(f"Exporting clean dataset to {output_dir}")
    df.to_csv(output_dir / 'complaints_cleaned.csv', index=False)
    logger.info("Export complete")

def generate_summary_stats(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate summary comparison stats.
    """
    summary = {
        'Raw Rows': len(df_raw),
        'Cleaned Rows': len(df_clean),
        'Rows Removed': len(df_raw) - len(df_clean),
        'Raw Columns': len(df_raw.columns),
        'Cleaned Columns': len(df_clean.columns),
        'Columns Added': len(df_clean.columns) - len(df_raw.columns)
    }
    return summary

def main() -> None:
    """
    Main cleaning pipeline execution.
    """
    logger.info("="*60)
    logger.info("STARTING ENTERPRISE DATA CLEANING PIPELINE")
    logger.info("="*60)

    # Paths
    project_root = Path.cwd()
    raw_data_path = project_root / 'data' / 'raw' / 'CFPB Complaints Data - Jan25 to Mar26.xlsx'
    output_dir = project_root / 'data' / 'processed'

    # 1. Load raw data
    df_raw = load_data(raw_data_path)

    # 2. Initial cleaning
    df_clean = df_raw.copy()
    for col in df_clean.columns:
        df_clean[col] = clean_text_column(df_clean[col])

    # 3. Date cleaning
    df_clean = clean_dates(df_clean)

    # 4. Standardize categories
    df_clean = standardize_categories(df_clean)

    # 5. Feature engineering
    df_clean = engineer_features(df_clean)

    # 6. Validate
    is_valid, issues = validate_data(df_clean)
    if not is_valid:
        logger.error(f"Validation failed: {issues}")
        raise Exception(f"Validation failed: {issues}")
    else:
        logger.info("Validation PASSED!")

    # 7. Export
    export_clean_dataset(df_clean, output_dir)

    # 8. Summary
    summary = generate_summary_stats(df_raw, df_clean)
    logger.info(f"Cleaning Summary: {summary}")
    logger.info("="*60)
    logger.info("DATA CLEANING PIPELINE COMPLETE")
    logger.info("="*60)

if __name__ == "__main__":
    main()
