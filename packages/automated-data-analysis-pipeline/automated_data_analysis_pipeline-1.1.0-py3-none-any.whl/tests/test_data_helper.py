import pandas as pd
import numpy as np


def load_data(file_path):
    """Load data from CSV or Excel file"""
    if file_path.endswith('.csv'):
        df2 = pd.read_csv(file_path)
        print(f"✅ Successfully loaded data with {df2.shape[0]} rows and {df2.shape[1]} columns")
        print("=== DATASET PREVIEW ===")
        print(df2.head())
        return df2
    elif file_path.endswith(('.xls', '.xlsx')):
        df2 = pd.read_excel(file_path)
        print(f"✅ Successfully loaded data with {df2.shape[0]} rows and {df2.shape[1]} columns")
        print("=== DATASET PREVIEW ===")
        print(df2.head())
        return df2
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")


def remove_duplicates(df):
    """Remove duplicate rows from DataFrame"""
    initial_rows = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = initial_rows - len(df)
    return df, removed


def handle_missing_values(df, threshold=0.7, fill_strategy=None):
    """Handle missing values based on specified threshold"""
    # Remove rows with more than threshold% missing values
    rows_initial = len(df)
    missing_per_row = df.isnull().mean(axis=1)
    df = df[missing_per_row <= threshold].reset_index(drop=True)
    rows_removed = rows_initial - len(df)

    # Fill remaining missing values
    fill_report = {}
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if fill_strategy and col in fill_strategy:
                # Use user-specified fill strategy
                if fill_strategy[col] == 'mean':
                    fill_value = df[col].mean()
                elif fill_strategy[col] == 'median':
                    fill_value = df[col].median()
                elif fill_strategy[col] == 'mode':
                    fill_value = df[col].mode()[0]
                else:
                    fill_value = fill_strategy[col]
            else:
                # Default strategy
                if np.issubdtype(df[col].dtype, np.number):
                    fill_value = df[col].mean()
                else:
                    fill_value = df[col].mode()[0] if not df[col].mode().empty else None

            df[col].fillna(fill_value, inplace=True)
            fill_report[col] = {
                'filled': df[col].isnull().sum(),
                'method': fill_strategy[col] if fill_strategy and col in fill_strategy else 'auto'
            }

    return df, rows_removed, fill_report


def check_data_format(df):
    """Check and attempt to fix data format issues"""
    format_issues = {}
    for col in df.columns:
        # Check numeric columns for non-numeric values
        if np.issubdtype(df[col].dtype, np.number):
            non_numeric = pd.to_numeric(df[col], errors='coerce').isna()
            if non_numeric.any():
                count = non_numeric.sum()
                format_issues[col] = f"{count} non-numeric values found in numeric column"

    return format_issues


def get_statistics(df, columns=None, stats=None):
    """Calculate statistics for specified columns"""
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns.tolist()
    if stats is None:
        stats = ['mean', 'median', 'std', 'min', 'max']

    results = {}
    for col in columns:
        if col in df.columns:
            col_stats = {}
            for stat in stats:
                if stat == 'mean':
                    col_stats[stat] = df[col].mean()
                elif stat == 'median':
                    col_stats[stat] = df[col].median()
                elif stat == 'std':
                    col_stats[stat] = df[col].std()
                elif stat == 'min':
                    col_stats[stat] = df[col].min()
                elif stat == 'max':
                    col_stats[stat] = df[col].max()
            results[col] = col_stats
    return results


def check_accuracy(df, date_columns=None):
    """Perform basic data accuracy checks"""
    accuracy_issues = {}

    # Check for numeric columns with zero values
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        zero_count = (df[col] == 0).sum()
        if zero_count > 0:
            accuracy_issues[col] = f"{zero_count} zero values found"

    return accuracy_issues


def generate_report(duplicates_removed, missing_rows_removed, fill_report,
                    format_issues, stats_results, accuracy_issues):
    """Generate terminal report"""
    print("\n=" * 50)
    print("DATA ANALYSIS REPORT".center(50))
    print("=" * 50)


    print("\n=== Data Cleaning Summary ===")
    print(f"Removed duplicates: {duplicates_removed} rows")
    print(f"Removed rows with >70% missing values: {missing_rows_removed} rows")

    if fill_report:
        print("\nMissing values filled:")
        for col, info in fill_report.items():
            print(f"- {col}: {info['filled']} values filled using {info['method']}")
    else:
        print("\nNo missing values found")

    if format_issues:
        print("\n=== Format Issues ===")
        for col, issue in format_issues.items():
            print(f"- {col}: {issue}")
    else:
        print("\nNo data format issues found")

    if stats_results:
        print("\n=== Statistical Summary ===")
        for col, stats in stats_results.items():
            print(f"\n{col}:")
            for stat, value in stats.items():
                print(f"  {stat}: {value:.2f}")

    if accuracy_issues:
        print("\n=== Accuracy Issues ===")
        for col, issue in accuracy_issues.items():
            print(f"- {col}: {issue}")
    else:
        print("\nNo accuracy issues found")

    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE".center(50))
    print("=" * 50)


def analyze_data(file_path, fill_strategy=None, stats_columns=None, stats=None):
    """Main function to automate data analysis process"""
    # Load data
    df = load_data(file_path)

    # Data cleaning
    df, duplicates_removed = remove_duplicates(df)
    df, missing_rows_removed, fill_report = handle_missing_values(df, fill_strategy=fill_strategy)

    # Data format checking
    format_issues = check_data_format(df)

    # Statistics calculation
    stats_results = get_statistics(df, columns=stats_columns, stats=stats)

    # Accuracy checks
    accuracy_issues = check_accuracy(df)

    # Generate report
    generate_report(
        duplicates_removed,
        missing_rows_removed,
        fill_report,
        format_issues,
        stats_results,
        accuracy_issues
    )

    return df
